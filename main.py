import json
import asyncio
import websockets

def printword(wordlist, firstword):
    for prior in wordlist:
        for wtidx, wordtype in enumerate(prior):
            if firstword in prior[wordtype]:
                print(wordtype)
                for idx, word in enumerate(prior[wordtype][firstword]):
                    if idx >= 5: break;
                    if wtidx == len(prior) and idx >= len(prior[wordtype][firstword]): return True;
                    print(word)
            else: break;
    return False;

def removeword(wordlist, fullword):
    for prior in wordlist:
        for wordtype in prior:
            if fullword[0] in prior[wordtype]:
                if prior[wordtype][fullword[0]].count(fullword) != 0:
                    prior[wordtype][fullword[0]].remove(fullword)
                    return True;
    return False;
def addword(f, wordlist, word):
    for prior in wordlist:
        if not "추가" in prior:
            prior["추가"] = {}
        if word[0] in prior["추가"]:
                print(word + " 추가됨")
                prior["추가"][word[0]].append(word)
        else:
            prior["추가"][word[0]] = []
            prior["추가"][word[0]].append(word)
            print(word + " 추가됨")
    f.close()
    f = open("kkutu.json", "w", encoding="utf-8")
    json.dump(wordlist, f, ensure_ascii=False)
    f.close()

async def main(websocket, path):
    f = open("kkutu.json", "r", encoding="utf-8")
    wordlist = []
    wordlist_orig = json.load(f)
    usedword = []
    mode = ""
    secondword = ""
    quit = False
    while quit == False:
        json_data = await websocket.recv()
        data = json.loads(json_data)
        if data["type"] == "game":
            mode = data["data"].split(" /")[0]
        elif data["type"] == "allowword":
            secondword = data["data"]
            printword(wordlist, secondword)
            secondword = ""
        elif data["type"] == "round":
            if mode == "한국어 끝말잇기":
                f.seek(0)
                wordlist = json.load(f)
                print("round change")
                printword(wordlist, data["data"])
        elif data["type"] == "history":
            if mode == "한국어 끝말잇기":
                firstword = data["data"][0]
                lastword = data["data"][len(data["data"])-1]
                if usedword.count(data["data"]) == 0:
                    usedword.append(data["data"])
                    if removeword(wordlist, data["data"]) == False:
                        addword(f, wordlist_orig, data["data"])
                        f = open("kkutu.json", "r", encoding="utf-8")
                        # for prior in wordlist_orig:
                        #     if not "추가" in prior:
                        #         prior["추가"] = {}
                        #     if data["data"][0] in prior["추가"]:
                        #             print(data["data"] + " 추가됨")
                        #             prior["추가"][data["data"][0]].append(data["data"])
                        #     else:
                        #         prior["추가"][data["data"][0]] = []
                        #         prior["추가"][data["data"][0]].append(data["data"])
                        #         print(data["data"] + " 추가됨")
                        # f.close()
                        # f = open("kkutu.json", "w", encoding="utf-8")
                        # json.dump(wordlist_orig, f, ensure_ascii=False)
                        # f.close()
                        # f = open("kkutu.json", "r", encoding="utf-8")
                    if printword(wordlist, lastword) == False and secondword != "":
                        printword(wordlist, secondword)
                        secondword = ""
        elif data["type"] == "lastword":
            addword(f, wordlist_orig, data["data"])
            f = open("kkutu.json", "r", encoding="utf-8")
    f.close()
start_server = websockets.serve(main, '127.0.0.1', 15678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
