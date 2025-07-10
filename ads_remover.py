```python
name = "Ads Remover"
description = """
Uklanja poznate reklame iz APK-a modifikovanjem poziva ka AdMob klasama i servisima (InterstitialAd, AdView, RewardedAd...).
"""

TARGET_CLASSES = [
    'com/google/android/gms/ads/',
    'com/facebook/ads/',
    'com/unity3d/ads/',
    'admob', 'ads', '/ads/'
]

def match(file_list):
    return any(any(k in f for k in TARGET_CLASSES) for f in file_list)

def apply_patch(smali_root):
    import os
    import shutil

    patched = 0

    for dirpath, _, filenames in os.walk(smali_root):
        for fn in filenames:
            if not fn.endswith(".smali"):
                continue
            path = os.path.join(dirpath, fn)
            with open(path, encoding="utf-8") as f:
                lines = f.readlines()

            new_lines = []
            modified = False
            inside_method = False

            for line in lines:
                if '.method' in line:
                    inside_method = True
                if inside_method and any(ad in line for ad in TARGET_CLASSES):
                    modified = True
                    continue  # skip ad-related line
                if '.end method' in line:
                    inside_method = False
                new_lines.append(line)

            if modified:
                with open(path, 'w', encoding="utf-8") as f:
                    f.writelines(new_lines)
                print(f"[-] Uklonjena reklama u: {path}")
                patched += 1

            # Bonus: DELETE datoteke koje očigledno sadrže samo reklame
            if any(ad in path.lower() for ad in TARGET_CLASSES):
                try:
                    os.remove(path)
                    print(f"[x] Obrisana ad klasa: {path}")
                    patched += 1
                except:
                    pass

    return patched
```

---