from pathlib import Path
import pandas as pd

EIS_COLUMNS = ["time", "cycle", "freq", "Re_Z", "neg_Im_Z", "Z_mag", "phase"]

def load_EIS(folder):
    eis_tables = []
    for txt_file in sorted(Path(folder).glob("*.txt")):
        dataframe = pd.read_csv(txt_file, sep="\t", skipinitialspace=True,
                                header=None, names=EIS_COLUMNS)
        dataframe = dataframe.apply(pd.to_numeric, errors="coerce").dropna()

        parts = txt_file.stem.split("_")
        state = parts[2]
        cell = parts[3]
        if cell == "25C42":
            cell = "25C04"

        dataframe["state"] = state
        dataframe["cell"] = cell
        eis_tables.append(dataframe)
    return pd.concat(eis_tables, ignore_index=True)

CAPACITY_COLUMNS = ["time", "cycle", "ox/red", "capacity"]

CAPACITY_COLUMNS = ["time", "cycle", "ox_red", "capacity"]

def load_Capacity(folder):
    capacity_tables = []
    for txt_file in sorted(Path(folder).glob("*.txt")):
        dataframe = pd.read_csv(txt_file, sep="\t", skipinitialspace=True,
                                header=None, names=CAPACITY_COLUMNS)
        dataframe = dataframe.apply(pd.to_numeric, errors="coerce").dropna()

        cell = txt_file.stem.split("_")[-1]

        dataframe["cell"] = cell
        capacity_tables.append(dataframe)
    return pd.concat(capacity_tables, ignore_index=True)


if __name__ == "__main__":
    df = load_EIS("EIS data")
    print(df.shape)
    print(df.groupby(["cell", "state"]).size())