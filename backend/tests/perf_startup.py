import time
import sys
import os
import importlib

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def measure_startup_time():
    print("Benchmark: Measuring Application Startup Time...")
    
    start_time = time.time()
    
    # Force import of main app which triggers all other imports
    try:
        if "app.main" in sys.modules:
            del sys.modules["app.main"]
        import app.main
    except Exception as e:
        print(f"❌ Startup Failed: {e}")
        return
        
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"⏱️ Startup Time: {duration:.4f} seconds")
    
    # Threshold check (e.g., must be under 2 seconds)
    if duration > 2.0:
        print(f"⚠️ WARNING: Startup too slow (Limit: 2.0s)")
    else:
        print(f"✅ Startup Performance OK")

if __name__ == "__main__":
    measure_startup_time()
