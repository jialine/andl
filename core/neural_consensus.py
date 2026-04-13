#!/usr/bin/env python3
"""
NeuralConsensus - Core Implementation
Distributed tamper-proof consensus mechanism for ANDL 2.0.1
Inspired by human brain's distributed memory and associative verification
"""

import numpy as np
import hashlib
import asyncio
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class ConsensusStatus(Enum):
    VALID = "valid"
    INVALID = "invalid"
    TAMPERED = "tampered"
    INCONCLUSIVE = "inconclusive"

@dataclass
class ShardInfo:
    """Vector shard information"""
    shard_id: int
    data: np.ndarray
    hash: str
    storage_nodes: List[str]

@dataclass
class VerificationPath:
    """Verification path result"""
    path_type: str  # temporal, semantic, causal
    nodes_verified: int
    nodes_supporting: int
    avg_similarity: float
    valid: bool

@dataclass
class ConsensusResult:
    """Final consensus result"""
    status: ConsensusStatus
    agreement_rate: float
    threshold: float
    paths: List[VerificationPath]
    tampered_shards: List[int]
    confidence: float

class SemanticEncoder:
    """
    Semantic vector encoder
    Converts text/intent to high-dimensional semantic vectors
    """
    
    def __init__(self, dimensions: int = 1024):
        self.dimensions = dimensions
        
    def encode(self, text: str) -> np.ndarray:
        """
        Encode text to semantic vector
        In production, use transformer-based model (BERT, etc.)
        """
        # Deterministic encoding for reproducibility
        np.random.seed(hash(text) % 2**32)
        vector = np.random.randn(self.dimensions).astype(np.float32)
        # Normalize
        vector = vector / np.linalg.norm(vector)
        return vector
    
    def decode(self, vector: np.ndarray) -> str:
        """
        Decode vector back to approximate text
        Note: This is approximate and for debugging only
        """
        return f"[Vector-{hash(vector.tobytes()) % 10000:04d}]"

class ConsensusNode:
    """
    NeuralConsensus node
    Stores vector shards and participates in verification
    """
    
    def __init__(self, node_id: str, reputation: float = 1.0):
        self.node_id = node_id
        self.shards: Dict[str, Dict] = {}
        self.reputation = reputation
        self.total_verifications = 0
        self.successful_verifications = 0
        
    async def store_shard(self, message_id: str, shard_id: int, 
                         shard_data: np.ndarray) -> bool:
        """Store a vector shard"""
        key = f"{message_id}_{shard_id}"
        self.shards[key] = {
            "data": shard_data.copy(),
            "hash": hashlib.sha256(shard_data.tobytes()).hexdigest(),
            "timestamp": asyncio.get_event_loop().time(),
            "access_count": 0
        }
        return True
    
    async def retrieve_shard(self, message_id: str, shard_id: int) -> Optional[np.ndarray]:
        """Retrieve a shard with simulated network reliability"""
        import random
        
        # Simulate 10% network failure rate
        if random.random() < 0.1:
            return None
            
        key = f"{message_id}_{shard_id}"
        if key in self.shards:
            self.shards[key]["access_count"] += 1
            return self.shards[key]["data"].copy()
        return None
    
    def verify_shard_integrity(self, message_id: str, shard_id: int,
                               claimed_data: np.ndarray) -> bool:
        """Verify shard integrity using hash"""
        key = f"{message_id}_{shard_id}"
        if key not in self.shards:
            return False
        
        stored_hash = self.shards[key]["hash"]
        claimed_hash = hashlib.sha256(claimed_data.tobytes()).hexdigest()
        return stored_hash == claimed_hash
    
    def update_reputation(self, success: bool):
        """Update node reputation based on verification success"""
        self.total_verifications += 1
        if success:
            self.successful_verifications += 1
            self.reputation = min(2.0, self.reputation + 0.01)
        else:
            self.reputation = max(0.1, self.reputation - 0.05)

class NeuralConsensus:
    """
    NeuralConsensus - Distributed tamper-proof verification
    
    Key features:
    1. Vector sharding - Split vector into semantic parts
    2. Distributed storage - Redundant storage across nodes
    3. Multi-path verification - Temporal, semantic, causal paths
    4. Cross-consensus - Agreement across multiple verification paths
    5. Dynamic correction - Detect and correct tampered data
    """
    
    def __init__(self, 
                 node_count: int = 5,
                 redundancy: int = 3,
                 consensus_threshold: float = 0.67,
                 shard_sizes: List[int] = None):
        
        self.nodes = [ConsensusNode(f"node_{i}") for i in range(node_count)]
        self.redundancy = redundancy
        self.consensus_threshold = consensus_threshold
        
        # Default shard sizes: intent(128), context(256), capability(512), meta(128)
        self.shard_sizes = shard_sizes or [128, 256, 512, 128]
        self.shard_names = ["intent", "context", "capability", "meta"]
        
        self.encoder = SemanticEncoder(sum(self.shard_sizes))
        
    def _decompose_vector(self, vector: np.ndarray) -> List[np.ndarray]:
        """Decompose vector into semantic shards"""
        shards = []
        start = 0
        for size in self.shard_sizes:
            shards.append(vector[start:start+size])
            start += size
        return shards
    
    def _reconstruct_vector(self, shards: List[np.ndarray]) -> np.ndarray:
        """Reconstruct vector from shards"""
        return np.concatenate(shards)
    
    async def store(self, vector: np.ndarray, message_id: str) -> Dict:
        """
        Distributed storage with redundancy
        
        Args:
            vector: Semantic vector to store
            message_id: Unique message identifier
            
        Returns:
            Storage metadata
        """
        shards = self._decompose_vector(vector)
        
        storage_tasks = []
        storage_plan = {}
        
        for i, shard in enumerate(shards):
            # Select storage nodes (weighted by reputation)
            import random
            weights = [n.reputation for n in self.nodes]
            total_weight = sum(weights)
            probs = [w/total_weight for w in weights]
            
            selected_nodes = np.random.choice(
                self.nodes, 
                size=min(self.redundancy, len(self.nodes)),
                replace=False,
                p=probs
            )
            
            storage_plan[i] = [n.node_id for n in selected_nodes]
            
            for node in selected_nodes:
                storage_tasks.append(node.store_shard(message_id, i, shard))
        
        await asyncio.gather(*storage_tasks)
        
        return {
            "message_id": message_id,
            "vector_hash": hashlib.sha256(vector.tobytes()).hexdigest()[:16],
            "shards_stored": len(shards),
            "redundancy": self.redundancy,
            "storage_plan": storage_plan
        }
    
    async def verify(self, message_id: str, claimed_vector: np.ndarray) -> ConsensusResult:
        """
        NeuralConsensus verification
        
        Args:
            message_id: Message to verify
            claimed_vector: Vector claiming to be the original
            
        Returns:
            ConsensusResult with verification status
        """
        # Initiate multi-path verification
        paths = await self._initiate_verification_paths(message_id)
        
        # Verify each path
        path_results = []
        for path in paths:
            result = await self._verify_path(path, claimed_vector)
            path_results.append(result)
        
        # Compute overall consensus
        consensus = self._compute_consensus(path_results)
        
        # Identify tampered shards if any
        tampered_shards = self._identify_tampered_shards(path_results)
        
        # Determine status
        if consensus["agreement"] >= self.consensus_threshold:
            status = ConsensusStatus.VALID
        elif consensus["agreement"] < 0.3:
            status = ConsensusStatus.TAMPERED
        else:
            status = ConsensusStatus.INVALID
        
        return ConsensusResult(
            status=status,
            agreement_rate=consensus["agreement"],
            threshold=self.consensus_threshold,
            paths=path_results,
            tampered_shards=tampered_shards,
            confidence=consensus["confidence"]
        )
    
    async def _initiate_verification_paths(self, message_id: str) -> List[Dict]:
        """Initiate multi-path associative retrieval"""
        paths = []
        
        # Path 1: Temporal (recent messages)
        temporal_nodes = [n for n in self.nodes 
                         if n.has_temporal_index(message_id)]
        paths.append({
            "type": "temporal",
            "nodes": temporal_nodes[:self.redundancy],
            "weight": 0.3
        })
        
        # Path 2: Semantic (similar vectors)
        semantic_nodes = [n for n in self.nodes 
                         if n.has_semantic_index(message_id)]
        paths.append({
            "type": "semantic", 
            "nodes": semantic_nodes[:self.redundancy],
            "weight": 0.4
        })
        
        # Path 3: Causal (related messages)
        causal_nodes = [n for n in self.nodes 
                       if n.has_causal_index(message_id)]
        paths.append({
            "type": "causal",
            "nodes": causal_nodes[:2],
            "weight": 0.3
        })
        
        return paths
    
    async def _verify_path(self, path: Dict, 
                          claimed_vector: np.ndarray) -> VerificationPath:
        """Verify a single path"""
        claimed_shards = self._decompose_vector(claimed_vector)
        
        node_results = []
        for node in path["nodes"]:
            similarities = []
            
            for shard_id in range(len(self.shard_sizes)):
                retrieved = await node.retrieve_shard("msg_001", shard_id)
                if retrieved is not None:
                    sim = self._cosine_similarity(
                        retrieved, 
                        claimed_shards[shard_id]
                    )
                    similarities.append(sim)
            
            if similarities:
                avg_sim = np.mean(similarities)
                node_results.append({
                    "node_id": node.node_id,
                    "similarity": avg_sim,
                    "valid": avg_sim > 0.85
                })
        
        valid_nodes = [r for r in node_results if r["valid"]]
        total_nodes = len(node_results)
        
        return VerificationPath(
            path_type=path["type"],
            nodes_verified=total_nodes,
            nodes_supporting=len(valid_nodes),
            avg_similarity=np.mean([r["similarity"] for r in node_results]) if node_results else 0,
            valid=len(valid_nodes) >= total_nodes * 0.5 if total_nodes > 0 else False
        )
    
    def _compute_consensus(self, path_results: List[VerificationPath]) -> Dict:
        """Compute overall consensus from path results"""
        if not path_results:
            return {"agreement": 0, "confidence": 0}
        
        valid_paths = sum(1 for p in path_results if p.valid)
        total_paths = len(path_results)
        
        agreement = valid_paths / total_paths
        
        # Confidence based on number of supporting nodes
        total_supporting = sum(p.nodes_supporting for p in path_results)
        total_verified = sum(p.nodes_verified for p in path_results)
        confidence = total_supporting / total_verified if total_verified > 0 else 0
        
        return {
            "agreement": agreement,
            "confidence": confidence,
            "valid_paths": valid_paths,
            "total_paths": total_paths
        }
    
    def _identify_tampered_shards(self, path_results: List[VerificationPath]) -> List[int]:
        """Identify which shards may be tampered"""
        # Simplified - in production, track per-shard verification
        tampered = []
        if all(not p.valid for p in path_results):
            tampered = list(range(len(self.shard_sizes)))
        return tampered
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Compute cosine similarity between two vectors"""
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return np.dot(a, b) / (norm_a * norm_b)
    
    async def correct_tampered_data(self, message_id: str, 
                                    tampered_shards: List[int]) -> Optional[np.ndarray]:
        """
        Attempt to correct tampered data using majority consensus
        """
        corrected_shards = []
        
        for shard_id in range(len(self.shard_sizes)):
            if shard_id in tampered_shards:
                # Retrieve from all nodes and take majority
                shard_versions = []
                for node in self.nodes:
                    retrieved = await node.retrieve_shard(message_id, shard_id)
                    if retrieved is not None:
                        shard_versions.append(retrieved)
                
                if shard_versions:
                    # Use mean as consensus (simplified)
                    corrected = np.mean(shard_versions, axis=0)
                    corrected_shards.append(corrected)
                else:
                    return None
            else:
                # Use any valid shard
                for node in self.nodes:
                    retrieved = await node.retrieve_shard(message_id, shard_id)
                    if retrieved is not None:
                        corrected_shards.append(retrieved)
                        break
        
        return self._reconstruct_vector(corrected_shards)

# Convenience functions for direct usage
async def store_secure(vector: np.ndarray, message_id: str, 
                       node_count: int = 5) -> Dict:
    """Convenience function for secure storage"""
    consensus = NeuralConsensus(node_count=node_count)
    return await consensus.store(vector, message_id)

async def verify_integrity(message_id: str, claimed_vector: np.ndarray,
                          node_count: int = 5) -> ConsensusResult:
    """Convenience function for integrity verification"""
    consensus = NeuralConsensus(node_count=node_count)
    return await consensus.verify(message_id, claimed_vector)

if __name__ == "__main__":
    # Simple test
    async def test():
        print("NeuralConsensus Core Implementation")
        print("=" * 50)
        
        consensus = NeuralConsensus(node_count=5)
        encoder = SemanticEncoder()
        
        # Store message
        vector = encoder.encode("Test message")
        result = await consensus.store(vector, "test_001")
        print(f"Storage result: {result}")
        
        # Verify
        verification = await consensus.verify("test_001", vector)
        print(f"Verification: {verification}")
    
    asyncio.run(test())
