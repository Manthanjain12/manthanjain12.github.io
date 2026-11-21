import os
import sys
import subprocess

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(base_dir, "healthcare_system", "backend")

    print("=" * 70)
    print("   OMNIHEALTH AI - HEALTHCARE RECOMMENDATION & CLINIC LOCATOR")
    print("   Non-Diagnostic Symptom Triage & Verified Clinic Directory")
    print("=" * 70)
    print("\n[+] Initializing database, NLP pipeline, and hospital registry...")
    print("[+] Launching unified web server on http://localhost:8000 ...")
    print("[+] Press Ctrl+C to terminate.\n")

    os.chdir(backend_dir)
    subprocess.run([sys.executable, "run_backend.py"])

if __name__ == "__main__":
    main()
