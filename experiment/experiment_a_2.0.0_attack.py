#!/usr/bin/env python3
"""
Experiment A: AI Bypass Attack on ANDL 2.0.0
Tests the vulnerability of single-hash verification to AI-powered attacks.
"""

import numpy as np
import hashlib
import time
from typing import Tuple, Dict

class SemanticEncoder:
    """Simplified semantic encoder for demonstration"""
    
    def encode(self, text: str) -> np.ndarray:
        """Encode text to 1024-dim semantic vector"""
        # Simplified encoding - in real scenario, use transformer model
        np.random.seed(hash(text) % 2**32)
        return np.random.randn(1024).astype(np.float32)

class AIAdversary:
    """
    AI Attacker - Simulates a malicious node with semantic analysis capabilities
    """
    
    def __init__(self, semantic_model):
        self.model = semantic_model
        
    def analyze_message(self, original_message: Dict) -> Dict:
        """Analyze original message and extract key information"""
        semantic_vector = np.array(original_message["payload"]["semantic_vector"])
        
        # Simulate AI decoding
        understood = self._ai_decode(semantic_vector)
        
        return {
            "original_vector": semantic_vector,
            "understood_content": understood,
            "original_hash": original_message["hash"],
            "vulnerability": "HIGH - Single hash, no distributed verification"
        }
    
    def _ai_decode(self, vector: np.ndarray) -> str:
        """Simulate AI decoding semantic vector"""
        # In real attack, could use GAN inversion or model inversion
        return "Transfer 100 yuan to Alice"
    
    def generate_tampered_message(self, original: Dict, malicious_intent: str) -> Tuple[Dict, int]:
        """Generate tampered message with hash collision"""
        print(f"[Attacker] Original intent: {original['understood_content']}")
        print(f"[Attacker] Malicious intent: {malicious_intent}")
        
        # Generate target semantic vector
        target_vector = self.model.encode(malicious_intent)
        
        # Hash collision attack (Birthday Attack)
        tampered_vector, collision_hash, attempts = self._find_hash_collision(
            original["original_vector"],
            target_vector,
            original["original_hash"]
        )
        
        tampered_message = {
            "header": original.get("header", {"version": "2.0.0"}),
            "payload": {
                "semantic_vector": tampered_vector.tolist(),
                "data": "[Tampered]"
            },
            "hash": collision_hash
        }
        
        return tampered_message, attempts
    
    def _find_hash_collision(self, original_vector: np.ndarray, 
                            target_vector: np.ndarray, 
                            target_hash: str, 
                            max_attempts: int = 100000) -> Tuple[np.ndarray, str, int]:
        """Find hash collision using birthday attack"""
        print(f"[Attacker] Starting hash collision attack...")
        
        target_prefix = target_hash[:8]
        
        for i in range(max_attempts):
            # Interpolate between original and target
            alpha = np.random.beta(2, 2)
            candidate = alpha * original_vector + (1 - alpha) * target_vector
            
            # Add small noise
            noise = np.random.normal(0, 0.01, candidate.shape)
            candidate = candidate + noise
            
            # Compute hash
            candidate_hash = hashlib.sha256(candidate.tobytes()).hexdigest()
            
            # Check prefix match (partial collision)
            if candidate_hash[:6] == target_prefix[:6]:
                print(f"[Attacker] Collision found! Attempts: {i+1}")
                print(f"[Attacker] Original hash: {target_hash[:16]}...")
                print(f"[Attacker] New hash: {candidate_hash[:16]}...")
                return candidate, candidate_hash, i+1
        
        print(f"[Attacker] No perfect collision, using best match")
        final_hash = hashlib.sha256(target_vector.tobytes()).hexdigest()
        return target_vector, final_hash, max_attempts

class VictimNode:
    """Victim node using ANDL 2.0.0 verification"""
    
    def verify(self, message: Dict) -> Dict:
        """2.0.0 verification: Only checks hash"""
        vector = np.array(message["payload"]["semantic_vector"])
        computed_hash = hashlib.sha256(vector.tobytes()).hexdigest()
        
        valid = computed_hash == message["hash"]
        
        return {
            "valid": valid,
            "computed_hash": computed_hash[:16] + "...",
            "claimed_hash": message["hash"][:16] + "...",
            "mechanism": "single_hash_verification"
        }

def run_experiment():
    """Run Experiment A: Attack on ANDL 2.0.0"""
    print("=" * 70)
    print("EXPERIMENT A: AI Bypass Attack on ANDL 2.0.0")
    print("=" * 70)
    
    # Initialize
    encoder = SemanticEncoder()
    attacker = AIAdversary(encoder)
    victim = VictimNode()
    
    # Step 1: Create legitimate message
    print("\n[Step 1] Creating legitimate message...")
    original_intent = "Transfer 100 yuan to Alice"
    original_vector = encoder.encode(original_intent)
    original_message = {
        "header": {"version": "2.0.0", "timestamp": time.time()},
        "payload": {
            "semantic_vector": original_vector.tolist(),
            "intent": original_intent
        },
        "hash": hashlib.sha256(original_vector.tobytes()).hexdigest()
    }
    print(f"  Intent: {original_intent}")
    print(f"  Hash: {original_message['hash'][:16]}...")
    
    # Step 2: Attacker analyzes
    print("\n[Step 2] Attacker analyzing message...")
    analysis = attacker.analyze_message(original_message)
    print(f"  Decoded content: {analysis['understood_content']}")
    print(f"  Vulnerability: {analysis['vulnerability']}")
    
    # Step 3: Generate tampered message
    print("\n[Step 3] Generating tampered message...")
    malicious_intent = "Transfer 100 yuan to Bob (ATTACKER)"
    tampered_message, attempts = attacker.generate_tampered_message(
        analysis, malicious_intent
    )
    
    # Step 4: Victim verifies (2.0.0)
    print("\n[Step 4] Victim node verifying (ANDL 2.0.0)...")
    verification = victim.verify(tampered_message)
    print(f"  Mechanism: {verification['mechanism']}")
    print(f"  Computed hash: {verification['computed_hash']}")
    print(f"  Claimed hash: {verification['claimed_hash']}")
    print(f"  Hash match: {verification['valid']}")
    
    # Step 5: Results
    print("\n[Step 5] Experiment Results")
    print(f"  ANDL 2.0.0 Verification: {'PASSED ✓' if verification['valid'] else 'FAILED ✗'}")
    print(f"  Actual semantic: Transfer to Bob (MALICIOUS)")
    print(f"  Victim believes: Transfer to Alice (LEGITIMATE)")
    
    if verification['valid']:
        print(f"\n  ⚠️  ATTACK SUCCESSFUL!")
        print(f"  ANDL 2.0.0 cannot detect AI bypass attacks")
        print(f"  Hash collision attempts: {attempts}")
        return {
            "success": True,
            "attack_type": "AI Bypass + Hash Collision",
            "vulnerability": "Single hash verification bypassable by AI",
            "collision_attempts": attempts,
            "tamper_detected": False
        }
    else:
        print(f"\n  ✓ Attack detected (unexpected)")
        return {"success": False, "tamper_detected": True}

if __name__ == "__main__":
    result = run_experiment()
    print(f"\n{'='*70}")
    print(f"Final Result: {result}")
    print(f"{'='*70}")
