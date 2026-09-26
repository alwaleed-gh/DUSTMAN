from pathlib import Path
from datetime import datetime, timedelta

def scan_directory(target_path: Path, max_age_days: int) -> tuple[int, float]:
    cutoff_time = datetime.now() - timedelta(days=max_age_days)
    total_files = 0
    total_bytes = 0

    print(f"\n📂 Checking directory: {target_path}")

    if not target_path.exists():
        print(f"   ⚠️ Directory does not exist.")
        return 0, 0.0

    try:
        for item in target_path.rglob("*"):
            if item.is_file():
                mtime = datetime.fromtimestamp(item.stat().st_mtime)
                if mtime < cutoff_time:
                    size = item.stat().st_size
                    total_files += 1
                    total_bytes += size
                    print(f"   [FLAGGED] {item.name} ({size / (1024 * 1024):.2f} MB)")

    except PermissionError:
        print(f"   ⚠️ Permission denied when accessing some files in {target_path}")

    total_mb = total_bytes / (1024 * 1024)
    if total_files == 0:
        print("   ℹ️ No files found matching the criteria.")
    else:
        print(f"   📊 Summary for {target_path.name}: {total_files} files, {total_mb:.2f} MB")

    return total_files, total_mb


def clean_directory(target_path: Path, max_age_days: int, dry_run: bool = True) -> tuple[int, float]:
    cutoff_time = datetime.now() - timedelta(days=max_age_days)
    deleted_files = 0
    deleted_bytes = 0

    print(f"\n🧹 Processing directory: {target_path}")

    if not target_path.exists():
        print(f"   ⚠️ Directory does not exist.")
        return 0, 0.0

    try:
        for item in target_path.rglob("*"):
            if item.is_file():
                mtime = datetime.fromtimestamp(item.stat().st_mtime)
                if mtime < cutoff_time:
                    size = item.stat().st_size
                    if not dry_run:
                        try:
                            item.unlink()
                            deleted_files += 1
                            deleted_bytes += size
                            print(f"   [DELETED] {item.name} ({size / (1024 * 1024):.2f} MB)")
                        except Exception as e:
                            print(f"   ❌ Failed to delete {item.name}: {e}")
                    else:
                        deleted_files += 1
                        deleted_bytes += size

    except PermissionError:
        print(f"   ⚠️ Permission denied when accessing some files in {target_path}")

    deleted_mb = deleted_bytes / (1024 * 1024)
    if deleted_files == 0:
        print("   ℹ️ No old files were deleted.")
    else:
        print(f"   ✅ Done: Removed {deleted_files} files, Freed {deleted_mb:.2f} MB")

    return deleted_files, deleted_mb