import ast, pathlib

REQUIRED = {
    "modules/vision/detector.py": "Detector",
    "modules/voice/wake_word.py": "WakeWordListener",
    "modules/voice/commander.py": "Commander",
    "modules/motion/simulator.py": "ArmSimulator",
    "modules/lighting/simulator.py": "LEDSimulator",
    "modules/heads/registry.py": "HeadRegistry",
}

def main():
    ok = True
    for path, cls in REQUIRED.items():
        f = pathlib.Path(path)
        if not f.exists():
            print(f"Missing files: {path}")
            ok = False
            continue
        names = [n.name for n in ast.parse(f.read_text(encoding="utf-8")).body
                 if isinstance(n, ast.ClassDef)]
        if cls in names:
            print(f"OK man, {path} -> {cls}")
        else:
            print(f"FAIL {path}: has {names}, expected {cls} wth dude")
            ok = False
    print("\nALL MODULES OK - run 'py main.py" if ok else "\nFic the FAIL/MISSING items.")

if __name__ == "__main__":
    main()