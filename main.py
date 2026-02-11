from core.engine import TalentAtlasEngine

def main():
    engine = TalentAtlasEngine("input.json")
    atlas = engine.run()
    engine.save(atlas)

if __name__ == "__main__":
    main()
