---
agents:
- none
category: chain
description: Graph RAG patterns, entity extraction with LLMs, relationship mapping,
  and Neo4j integration
knowledge:
- none
name: managing-knowledge-graphs
related_skills:
- none
templates:
- none
tools:
- none
type: skill
version: 1.0.0
---
# Knowledge Graphs

Graph RAG patterns, entity extraction with LLMs, relationship mapping, and Neo4j integration

Build knowledge graphs for RAG systems using entity extraction, relationship mapping, and graph databases like Neo4j.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Entity Extraction with LLMs

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List, Optional
import json

class Entity(BaseModel):
    """Entity model."""
    name: str = Field(description="Entity name")
    type: str = Field(description="Entity type (Person, Organization, Concept, etc.)")
    description: Optional[str] = Field(default=None, description="Brief description")

class Relationship(BaseModel):
    """Relationship model."""
    source: str = Field(description="Source entity name")
    target: str = Field(description="Target entity name")
    relationship_type: str = Field(description="Type of relationship")
    description: Optional[str] = Field(default=None, description="Relationship description")

class KnowledgeGraph(BaseModel):
    """Knowledge graph structure."""
    entities: List[Entity] = Field(description="List of entities")
    relationships: List[Relationship] = Field(description="List of relationships")

class EntityExtractor:
    """Extract entities and relationships using LLMs."""

    def __init__(self, model: str = "gemini-2.5-flash"):
        self.llm = ChatGoogleGenerativeAI(model=model)

    def extract_from_text(self, text: str) -> KnowledgeGraph:
        """Extract entities and relationships from text."""
        prompt = PromptTemplate(
            template="""Extract entities and relationships from the following text.

Text: {text}

Return a JSON object with:
- "entities": [{{"name": "...", "type": "...", "description": "..."}}]
- "relationships": [{{"source": "...", "target": "...", "relationship_type": "...", "description": "..."}}]

Focus on:
- Named entities (people, organizations, locations, concepts)
- Clear relationships between entities
- Important facts and connections

JSON:""",
            input_variables=["text"]
        )

        chain = prompt | self.llm
        response = chain.invoke({"text": text})

        # Parse JSON
        try:
            data = json.loads(response.content)
            return KnowledgeGraph(**data)
        except:
            # Fallback: try structured output
            return self._extract_structured(text)

    def _extract_structured(self, text: str) -> KnowledgeGraph:
        """Extract using structured output."""
        from langchain_core.output_parsers import PydanticOutputParser

        parser = PydanticOutputParser(pydantic_object=KnowledgeGraph)

        prompt = PromptTemplate(
            template="""Extract entities and relationships from the text.

Text: {text}

{format_instructions}""",
            input_variables=["text"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )

        chain = prompt | self.llm | parser
        return chain.invoke({"text": text})

# Usage
extractor = EntityExtractor()
text = "Apple Inc. was founded by Steve Jobs. Tim Cook is the current CEO."
kg = extractor.extract_from_text(text)
```

### Step 2: Building Knowledge Graph

```python
from typing import Dict, List, Set
from dataclasses import dataclass

@dataclass
class Entity:
    """Entity in knowledge graph."""
    id: str
    name: str
    type: str
    properties: Dict = None

    def __post_init__(self):
        if self.properties is None:
            self.properties = {}

@dataclass
class Relationship:
    """Relationship in knowledge graph."""
    source_id: str
    target_id: str
    relationship_type: str
    properties: Dict = None

    def __post_init__(self):
        if self.properties is None:
            self.properties = {}

class KnowledgeGraphBuilder:
    """Build and manage knowledge graph."""

    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.relationships: List[Relationship] = []
        self.entity_index: Dict[str, str] = {}  # name -> id mapping

    def add_entity(self, name: str, entity_type: str, properties: Dict = None) -> str:
        """Add entity to graph."""
        # Check if exists
        if name in self.entity_index:
            entity_id = self.entity_index[name]
            # Update properties
            if properties:
                self.entities[entity_id].properties.update(properties)
            return entity_id

        # Create new entity
        entity_id = f"{entity_type}_{len(self.entities)}"
        entity = Entity(
            id=entity_id,
            name=name,
            type=entity_type,
            properties=properties or {}
        )

        self.entities[entity_id] = entity
        self.entity_index[name] = entity_id

        return entity_id

    def add_relationship(self, source_name: str, target_name: str,
                        relationship_type: str, properties: Dict = None):
        """Add relationship to graph."""
        # Get or create entities
        source_id = self.entity_index.get(source_name)
        if not source_id:
            source_id = self.add_entity(source_name, "Unknown")

        target_id = self.entity_index.get(target_name)
        if not target_id:
            target_id = self.add_entity(target_name, "Unknown")

        # Create relationship
        rel = Relationship(
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            properties=properties or {}
        )

        self.relationships.append(rel)

    def merge_kg(self, kg: KnowledgeGraph):
        """Merge extracted knowledge graph into builder."""
        # Add entities
        for entity in kg.entities:
            self.add_entity(
                name=entity.name,
                entity_type=entity.type,
                properties={"description": entity.description} if entity.description else {}
            )

        # Add relationships
        for rel in kg.relationships:
            self.add_relationship(
                source_name=rel.source,
                target_name=rel.target,
                relationship_type=rel.relationship_type,
                properties={"description": rel.description} if rel.description else {}
            )

    def get_entity_neighbors(self, entity_name: str) -> List[Entity]:
        """Get entities connected to given entity."""
        entity_id = self.entity_index.get(entity_name)
        if not entity_id:
            return []

        neighbor_ids = set()
        for rel in self.relationships:
            if rel.source_id == entity_id:
                neighbor_ids.add(rel.target_id)
            elif rel.target_id == entity_id:
                neighbor_ids.add(rel.source_id)

        return [self.entities[eid] for eid in neighbor_ids if eid in self.entities]

    def to_dict(self) -> Dict:
        """Convert to dictionary format."""
        return {
            "entities": [
                {
                    "id": e.id,
                    "name": e.name,
                    "type": e.type,
                    "properties": e.properties
                }
                for e in self.entities.values()
            ],
            "relationships": [
                {
                    "source": r.source_id,
                    "target": r.target_id,
                    "type": r.relationship_type,
                    "properties": r.properties
                }
                for r in self.relationships
            ]
        }
```

### Step 3: Neo4j Integration

```python
from neo4j import GraphDatabase
from typing import List, Dict

class Neo4jKnowledgeGraph:
    """Knowledge graph stored in Neo4j."""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """Close database connection."""
        self.driver.close()

    def create_entity(self, name: str, entity_type: str, properties: Dict = None):
        """Create entity node."""
        with self.driver.session() as session:
            props = properties or {}
            props["name"] = name
            props["type"] = entity_type

            query = """
            MERGE (e:Entity {name: $name})
            SET e.type = $type
            SET e += $properties
            RETURN e
            """

            session.run(query, name=name, type=entity_type, properties=props)

    def create_relationship(self, source_name: str, target_name: str,
                           relationship_type: str, properties: Dict = None):
        """Create relationship between entities."""
        with self.driver.session() as session:
            props = properties or {}

            query = f"""
            MATCH (source:Entity {{name: $source_name}})
            MATCH (target:Entity {{name: $target_name}})
            MERGE (source)-[r:{relationship_type}]->(target)
            SET r += $properties
            RETURN r
            """

            session.run(query,
                       source_name=source_name,
                       target_name=target_name,
                       properties=props)

    def query_entities(self, entity_type: str = None, limit: int = 100) -> List[Dict]:
        """Query entities."""
        with self.driver.session() as session:
            if entity_type:
                query = """
                MATCH (e:Entity {type: $type})
                RETURN e.name as name, e.type as type, properties(e) as properties
                LIMIT $limit
                """
                result = session.run(query, type=entity_type, limit=limit)
            else:
                query = """
                MATCH (e:Entity)
                RETURN e.name as name, e.type as type, properties(e) as properties
                LIMIT $limit
                """
                result = session.run(query, limit=limit)

            return [record.data() for record in result]

    def find_path(self, source_name: str, target_name: str, max_depth: int = 3) -> List[List[Dict]]:
        """Find paths between entities."""
        with self.driver.session() as session:
            query = """
            MATCH path = shortestPath(
                (source:Entity {name: $source_name})-[*1..{max_depth}]-(target:Entity {name: $target_name})
            )
            RETURN [node in nodes(path) | node.name] as path
            """

            result = session.run(query,
                                source_name=source_name,
                                target_name=target_name,
                                max_depth=max_depth)

            return [record["path"] for record in result]

    def get_entity_context(self, entity_name: str, depth: int = 2) -> Dict:
        """Get entity with surrounding context."""
        with self.driver.session() as session:
            query = f"""
            MATCH (e:Entity {{name: $name}})
            MATCH path = (e)-[*1..{depth}]-(connected)
            RETURN e, collect(DISTINCT connected) as connections,
                   collect(DISTINCT relationships(path)) as relationships
            """

            result = session.run(query, name=entity_name)
            record = result.single()

            if record:
                return {
                    "entity": dict(record["e"]),
                    "connections": [dict(c) for c in record["connections"]],
                    "relationships": [dict(r) for rels in record["relationships"] for r in rels]
                }
            return {}

# Usage
neo4j_kg = Neo4jKnowledgeGraph("bolt://localhost:7687", "neo4j", "password")
neo4j_kg.create_entity("Apple Inc.", "Organization", {"founded": 1976})
neo4j_kg.create_entity("Steve Jobs", "Person")
neo4j_kg.create_relationship("Steve Jobs", "Apple Inc.", "FOUNDED")
```

### Step 4: Graph RAG Patterns

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from typing import List, Dict

class GraphRAG:
    """RAG system using knowledge graph."""

    def __init__(self, neo4j_kg: Neo4jKnowledgeGraph):
        self.kg = neo4j_kg
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    def extract_query_entities(self, query: str) -> List[str]:
        """Extract entity names from query."""
        prompt = PromptTemplate(
            template="""Extract entity names from this query. Return only the entity names, comma-separated.

Query: {query}

Entities:""",
            input_variables=["query"]
        )

        chain = prompt | self.llm
        response = chain.invoke({"query": query})

        entities = [e.strip() for e in response.content.split(",")]
        return entities

    def retrieve_subgraph(self, entity_names: List[str], depth: int = 2) -> Dict:
        """Retrieve subgraph around entities."""
        all_entities = set()
        all_relationships = []

        for entity_name in entity_names:
            context = self.kg.get_entity_context(entity_name, depth=depth)
            if context:
                all_entities.add(context["entity"]["name"])
                for conn in context["connections"]:
                    all_entities.add(conn["name"])
                all_relationships.extend(context["relationships"])

        return {
            "entities": list(all_entities),
            "relationships": all_relationships
        }

    def answer_with_graph(self, query: str) -> Dict:
        """Answer query using knowledge graph context."""
        # Extract entities
        entities = self.extract_query_entities(query)

        if not entities:
            return {"answer": "No entities found in query", "entities": []}

        # Retrieve subgraph
        subgraph = self.retrieve_subgraph(entities)

        # Format context
        entities_str = ", ".join(subgraph["entities"])
        relationships_str = "\n".join([
            f"- {r.get('source', {}).get('name', '')} {r.get('type', '')} {r.get('target', {}).get('name', '')}"
            for r in subgraph["relationships"]
        ])

        context = f"""Knowledge Graph Context:

Entities: {entities_str}

Relationships:
{relationships_str}"""

        # Generate answer
        prompt = PromptTemplate(
            template="""Answer the question using the knowledge graph context.

{context}

Question: {query}

Answer:""",
            input_variables=["context", "query"]
        )

        chain = prompt | self.llm
        answer = chain.invoke({"context": context, "query": query})

        return {
            "answer": answer.content if hasattr(answer, "content") else str(answer),
            "entities": entities,
            "subgraph": subgraph
        }
```

### Step 5: Entity Resolution and Merging

```python
class EntityResolver:
    """Resolve and merge duplicate entities."""

    def __init__(self, llm):
        self.llm = llm

    def find_duplicates(self, entities: List[Entity], threshold: float = 0.8) -> List[List[str]]:
        """Find potential duplicate entities."""
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")

        # Embed entity names
        names = [e.name for e in entities]
        embeddings = model.encode(names)

        # Find similar pairs
        duplicates = []
        seen = set()

        for i, entity1 in enumerate(entities):
            if entity1.name in seen:
                continue

            group = [entity1.name]

            for j, entity2 in enumerate(entities[i+1:], i+1):
                similarity = self._cosine_similarity(embeddings[i], embeddings[j])
                if similarity >= threshold:
                    group.append(entity2.name)
                    seen.add(entity2.name)

            if len(group) > 1:
                duplicates.append(group)
                seen.add(entity1.name)

        return duplicates

    def _cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity."""
        import numpy as np
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def merge_entities(self, entity_groups: List[List[str]], kg_builder: KnowledgeGraphBuilder):
        """Merge duplicate entities."""
        for group in entity_groups:
            if len(group) < 2:
                continue

            # Use first entity as canonical
            canonical = group[0]
            duplicates = group[1:]

            # Get canonical entity ID
            canonical_id = kg_builder.entity_index.get(canonical)

            # Merge relationships
            for duplicate_name in duplicates:
                duplicate_id = kg_builder.entity_index.get(duplicate_name)
                if not duplicate_id:
                    continue

                # Update relationships
                for rel in kg_builder.relationships:
                    if rel.source_id == duplicate_id:
                        rel.source_id = canonical_id
                    if rel.target_id == duplicate_id:
                        rel.target_id = canonical_id

                # Remove duplicate entity
                if duplicate_id in kg_builder.entities:
                    del kg_builder.entities[duplicate_id]
                if duplicate_name in kg_builder.entity_index:
                    del kg_builder.entity_index[duplicate_name]
```

### Step 6: Complete Graph RAG System

```python
class CompleteGraphRAG:
    """Complete graph RAG system."""

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        self.neo4j_kg = Neo4jKnowledgeGraph(neo4j_uri, neo4j_user, neo4j_password)
        self.extractor = EntityExtractor()
        self.graph_rag = GraphRAG(self.neo4j_kg)
        self.builder = KnowledgeGraphBuilder()

    def ingest_documents(self, documents: List[str]):
        """Ingest documents and build knowledge graph."""
        for doc_text in documents:
            # Extract entities and relationships
            kg = self.extractor.extract_from_text(doc_text)

            # Merge into builder
            self.builder.merge_kg(kg)

        # Resolve duplicates
        resolver = EntityResolver(self.graph_rag.llm)
        duplicates = resolver.find_duplicates(list(self.builder.entities.values()))
        resolver.merge_entities(duplicates, self.builder)

        # Store in Neo4j
        for entity in self.builder.entities.values():
            self.neo4j_kg.create_entity(
                entity.name,
                entity.type,
                entity.properties
            )

        for rel in self.builder.relationships:
            source_name = self.builder.entities[rel.source_id].name
            target_name = self.builder.entities[rel.target_id].name
            self.neo4j_kg.create_relationship(
                source_name,
                target_name,
                rel.relationship_type,
                rel.properties
            )

    def query(self, question: str) -> Dict:
        """Query the graph RAG system."""
        return self.graph_rag.answer_with_graph(question)

    def close(self):
        """Close connections."""
        self.neo4j_kg.close()
```

## Knowledge Graph Patterns

| Pattern | Use Case | Pros | Cons |
|---------|----------|------|------|
| LLM Extraction | Unstructured text | High quality | Slower, costs |
| Rule-based | Structured data | Fast, precise | Limited coverage |
| Hybrid | Mixed sources | Best of both | More complex |
| Graph RAG | Entity queries | Structured answers | Requires graph DB |

## Best Practices

- Use LLMs for entity extraction from unstructured text
- Store entities with rich metadata (type, properties)
- Resolve duplicate entities before storing
- Use graph databases (Neo4j) for complex queries
- Extract relationships explicitly, not just entities
- Use subgraph retrieval for focused context
- Maintain entity canonicalization
- Index entities for fast lookup

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| No entity resolution | Merge duplicates before storage |
| Ignoring relationships | Extract and store relationships |
| Flat entity storage | Use graph database |
| No metadata | Store entity types and properties |
| Single extraction pass | Iteratively refine graph |
| No canonicalization | Resolve entity variants |
| Ignoring graph structure | Use graph queries for retrieval |

## Related

- Skill: `applying-rag-patterns`
- Skill: `retrieving-advanced`
- Skill: `vision-agents`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
