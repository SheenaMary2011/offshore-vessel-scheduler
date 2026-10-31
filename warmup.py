def warmup():
    storm = [3,7]
    for d in range(1,11):
        if d in storm:
            print(f"Day {d} :STORM")
        else:
            print(f"Day {d} :calm")



warmup()