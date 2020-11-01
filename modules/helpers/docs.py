from bson import ObjectId


def list_docs(documents):
    info = []
    for doc in documents:
        c = list(doc.values())
        c[0] = str(c[0].generation_time).split('+')[0]
        info.append(c)
    return info


def prep_docs_to_report(lists):
    for lst in lists:
        lst.pop(1)
        lst.pop(1)
    return lists


if __name__ == "__main__":
    data = [{"_id": ObjectId('5f34418b9d0bb937a2108ac0'),
             "product": "Vancomycin Hydrochloride",
             "lot": "2001039.1",
             "tray": "T0104",
             "vials": "287"
             },
            {"_id": ObjectId('5f34418b9d0bb937a2108ac1'),
             "product": "Vancomycin Hydrochloride",
             "lot": "2001039.1",
             "tray": "T0105",
             "vials": "180"
             }]
    info = []
    for doc in data:
        c = list(doc.values())
        print(c)
        c[0] = str(c[0].generation_time).split('+')[0]
        info.append(c)
    print(info)
    prep_docs_to_report(info)

    print("done")