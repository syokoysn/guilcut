import guilcut
import time

if __name__ == "__main__":
    # データの取得

    # dataset = guilcut.datasets.load_roadef2018(kind="B", number=10)

    dataset = guilcut.datasets.load_roadef2018(kind="B", number=15)
    # 前処理
    # itemのdf
    batch_df = dataset["batch"]
    # defectのdf
    defect_df = dataset["defect"]
    #
    s = time.time()
    # TODO: 関数化する
    for i in range(len(batch_df)):
        a, b = batch_df.LENGTH_ITEM[i], batch_df.WIDTH_ITEM[i]
        if a >= b:
            pass
        else:
            batch_df.at[i, "LENGTH_ITEM"] = b
            batch_df.at[i, "WIDTH_ITEM"] = a

    w_data = batch_df.WIDTH_ITEM.to_dict()
    h_data = batch_df.LENGTH_ITEM.to_dict()
    area_flag = batch_df.LENGTH_ITEM * batch_df.WIDTH_ITEM

    e = time.time()
    print(e - s)
    # 求解
    # 結果の表示
    print(dataset)
    print("print")
