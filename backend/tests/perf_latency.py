import asyncio
import httpx
import time
import sys
import os

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# We assume the app is running locally for this test, 
# or we can test using TestClient for "internal" latency excluding network.
from fastapi.testclient import TestClient
from app.main import app

def benchmark_health_endpoint(requests_count=100):
    print(f"Benchmark: Measuring Latency for {requests_count} concurrent requests...")
    
    client = TestClient(app)
    
    start_time = time.time()
    errors = 0
    
    # Using TestClient acts synchronously blocking, 
    # for true concurrency we'd need uvicorn running separate.
    # But this measures 'app processing time' efficiently.
    
    latencies = []
    
    for _ in range(requests_count):
        req_start = time.time()
        response = client.get("/health")
        req_end = time.time()
        latencies.append((req_end - req_start) * 1000) # ms
        
        if response.status_code != 200:
            errors += 1
            
    end_time = time.time()
    total_time = end_time - start_time
    
    avg_latency = sum(latencies) / len(latencies)
    max_latency = max(latencies)
    min_latency = min(latencies)
    
    # Calculate p95
    latencies.sort()
    p95_index = int(0.95 * len(latencies))
    p95_latency = latencies[p95_index]
    
    print(f"📊 Results:")
    print(f"   Total Time: {total_time:.4f}s")
    print(f"   Avg Latency: {avg_latency:.2f}ms")
    print(f"   Min Latency: {min_latency:.2f}ms")
    print(f"   Max Latency: {max_latency:.2f}ms")
    print(f"   P95 Latency: {p95_latency:.2f}ms")
    print(f"   Errors:      {errors}")
    
    if p95_latency > 50:
        print("⚠️ WARNING: P95 Latency > 50ms")
    else:
        print("✅ Latency Performance OK")

if __name__ == "__main__":
    benchmark_health_endpoint()
