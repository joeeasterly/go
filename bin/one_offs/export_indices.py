#!/usr/bin/env python3
import pymongo
from bson import ObjectId
from datetime import datetime
import json

def connect_mungo():
    client = pymongo.MongoClient("mungo:27017")
    db = client["go"]
    collection = db["link"]
    return collection

# Function to handle ObjectId serialization
def handle_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

# Initialize MongoDB client and connect to the database
collection = connect_mungo()

# Your array of prefixes
prefixes = [
    "11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","1g","1h","1j","1k","1m","1n","1p","1q","1r","1s","1t","1u","1v","1w","1x","1y","1z",
    "21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","2g","2h","2j","2k","2m","2n","2p","2q","2r","2s","2t","2u","2v","2w","2x","2y","2z",
    "31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","3g","3h","3j","3k","3m","3n","3p","3q","3r","3s","3t","3u","3v","3w","3x","3y","3z",
    "41","42","43","44","45","46","47","48","49","4a","4b","4c","4d","4e","4f","4g","4h","4j","4k","4m","4n","4p","4q","4r","4s","4t","4u","4v","4w","4x","4y","4z",
    "51","52","53","54","55","56","57","58","59","5a","5b","5c","5d","5e","5f","5g","5h","5j","5k","5m","5n","5p","5q","5r","5s","5t","5u","5v","5w","5x","5y","5z",
    "61","62","63","64","65","66","67","68","69","6a","6b","6c","6d","6e","6f","6g","6h","6j","6k","6m","6n","6p","6q","6r","6s","6t","6u","6v","6w","6x","6y","6z",
    "71","72","73","74","75","76","77","78","79","7a","7b","7c","7d","7e","7f","7g","7h","7j","7k","7m","7n","7p","7q","7r","7s","7t","7u","7v","7w","7x","7y","7z",
    "81","82","83","84","85","86","87","88","89","8a","8b","8c","8d","8e","8f","8g","8h","8j","8k","8m","8n","8p","8q","8r","8s","8t","8u","8v","8w","8x","8y","8z",
    "91","92","93","94","95","96","97","98","99","9a","9b","9c","9d","9e","9f","9g","9h","9j","9k","9m","9n","9p","9q","9r","9s","9t","9u","9v","9w","9x","9y","9z",
    "a1","a2","a3","a4","a5","a6","a7","a8","a9","aa","ab","ac","ad","ae","af","ag","ah","aj","ak","am","an","ap","aq","ar","as","at","au","av","aw","ax","ay","az",
    "b1","b2","b3","b4","b5","b6","b7","b8","b9","ba","bb","bc","bd","be","bf","bg","bh","bj","bk","bm","bn","bp","bq","br","bs","bt","bu","bv","bw","bx","by","bz",
    "c1","c2","c3","c4","c5","c6","c7","c8","c9","ca","cb","cc","cd","ce","cf","cg","ch","cj","ck","cm","cn","cp","cq","cr","cs","ct","cu","cv","cw","cx","cy","cz",
    "d1","d2","d3","d4","d5","d6","d7","d8","d9","da","db","dc","dd","de","df","dg","dh","dj","dk","dm","dn","dp","dq","dr","ds","dt","du","dv","dw","dx","dy","dz",
    "e1","e2","e3","e4","e5","e6","e7","e8","e9","ea","eb","ec","ed","ee","ef","eg","eh","ej","ek","em","en","ep","eq","er","es","et","eu","ev","ew","ex","ey","ez",
    "f1","f2","f3","f4","f5","f6","f7","f8","f9","fa","fb","fc","fd","fe","ff","fg","fh","fj","fk","fm","fn","fp","fq","fr","fs","ft","fu","fv","fw","fx","fy","fz",
    "g1","g2","g3","g4","g5","g6","g7","g8","g9","ga","gb","gc","gd","ge","gf","gg","gh","gj","gk","gm","gn","gp","gq","gr","gs","gt","gu","gv","gw","gx","gy","gz",
    "h1","h2","h3","h4","h5","h6","h7","h8","h9","ha","hb","hc","hd","he","hf","hg","hh","hj","hk","hm","hn","hp","hq","hr","hs","ht","hu","hv","hw","hx","hy","hz",
    "j1","j2","j3","j4","j5","j6","j7","j8","j9","ja","jb","jc","jd","je","jf","jg","jh","jj","jk","jm","jn","jp","jq","jr","js","jt","ju","jv","jw","jx","jy","jz",
    "k1","k2","k3","k4","k5","k6","k7","k8","k9","ka","kb","kc","kd","ke","kf","kg","kh","kj","kk","km","kn","kp","kq","kr","ks","kt","ku","kv","kw","kx","ky","kz",
    "m1","m2","m3","m4","m5","m6","m7","m8","m9","ma","mb","mc","md","me","mf","mg","mh","mj","mk","mm","mn","mp","mq","mr","ms","mt","mu","mv","mw","mx","my","mz",
    "n1","n2","n3","n4","n5","n6","n7","n8","n9","na","nb","nc","nd","ne","nf","ng","nh","nj","nk","nm","nn","np","nq","nr","ns","nt","nu","nv","nw","nx","ny","nz",
    "p1","p2","p3","p4","p5","p6","p7","p8","p9","pa","pb","pc","pd","pe","pf","pg","ph","pj","pk","pm","pn","pp","pq","pr","ps","pt","pu","pv","pw","px","py","pz",
    "q1","q2","q3","q4","q5","q6","q7","q8","q9","qa","qb","qc","qd","qe","qf","qg","qh","qj","qk","qm","qn","qp","qq","qr","qs","qt","qu","qv","qw","qx","qy","qz",
    "r1","r2","r3","r4","r5","r6","r7","r8","r9","ra","rb","rc","rd","re","rf","rg","rh","rj","rk","rm","rn","rp","rq","rr","rs","rt","ru","rv","rw","rx","ry","rz",
    "s1","s2","s3","s4","s5","s6","s7","s8","s9","sa","sb","sc","sd","se","sf","sg","sh","sj","sk","sm","sn","sp","sq","sr","ss","st","su","sv","sw","sx","sy","sz",
    "t1","t2","t3","t4","t5","t6","t7","t8","t9","ta","tb","tc","td","te","tf","tg","th","tj","tk","tm","tn","tp","tq","tr","ts","tt","tu","tv","tw","tx","ty","tz",
    "u1","u2","u3","u4","u5","u6","u7","u8","u9","ua","ub","uc","ud","ue","uf","ug","uh","uj","uk","um","un","up","uq","ur","us","ut","uu","uv","uw","ux","uy","uz",
    "v1","v2","v3","v4","v5","v6","v7","v8","v9","va","vb","vc","vd","ve","vf","vg","vh","vj","vk","vm","vn","vp","vq","vr","vs","vt","vu","vv","vw","vx","vy","vz",
    "w1","w2","w3","w4","w5","w6","w7","w8","w9","wa","wb","wc","wd","we","wf","wg","wh","wj","wk","wm","wn","wp","wq","wr","ws","wt","wu","wv","ww","wx","wy","wz",
    "x1","x2","x3","x4","x5","x6","x7","x8","x9","xa","xb","xc","xd","xe","xf","xg","xh","xj","xk","xm","xn","xp","xq","xr","xs","xt","xu","xv","xw","xx","xy","xz",
    "y1","y2","y3","y4","y5","y6","y7","y8","y9","ya","yb","yc","yd","ye","yf","yg","yh","yj","yk","ym","yn","yp","yq","yr","ys","yt","yu","yv","yw","yx","yy","yz",
    "z1","z2","z3","z4","z5","z6","z7","z8","z9","za","zb","zc","zd","ze","zf","zg","zh","zj","zk","zm","zn","zp","zq","zr","zs","zt","zu","zv","zw","zx","zy","zz"
]

# Loop through each prefix and find matching documents
for prefix in prefixes:
    # Fetch documents whose identifiers start with the current prefix
    results = collection.find({"identifier": {'$regex': f'^{prefix}'}})

    # Create a list to hold the documents
    documents_list = []

    for result in results:
        # Convert each document's ObjectId to a string
        result['_id'] = str(result['_id'])
        documents_list.append(result)


    # Export the list of documents to a JSON file
    first_char = prefix[0]
    second_char = prefix[1]
    file_path = f'/usr/local/gh/go/data/{first_char}/{second_char}/{prefix}.json'
    with open(f'/usr/local/gh/go/data/{first_char}/{second_char}/{prefix}.json', 'w') as f:
        json.dump(documents_list, f, default=handle_objectid, indent=4)
        print(f'Exported {file_path}')