# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 20:17:01 2018

@author: chhabriv
"""
import os,sys
import secretsharing as sss

# for JSON output
import jsonpickle # install via  "$ sudo pip install -U jsonpickle"
# for hashing passwords
from hashlib import sha256

# for encrypting you need: sudo -H pip install pycrypto
import base64
from Crypto.Cipher import AES

# our cs7ns1-specific functions for shamir-like sharing

def pxor(pwd,share):
    '''
      XOR a hashed password into a Shamir-share

      1st few chars of share are index, then "-" then hexdigits
      we'll return the same index, then "-" then xor(hexdigits,sha256(pwd))
      we truncate the sha256(pwd) to if the hexdigits are shorter
      we left pad the sha256(pwd) with zeros if the hexdigits are longer
      we left pad the output with zeros to the full length we xor'd
    '''
    words=share.split("-")
    hexshare=words[1]
    slen=len(hexshare)
    hashpwd=sha256(pwd).hexdigest()
    hlen=len(hashpwd)
    outlen=0
    if slen<hlen:
        outlen=slen
        hashpwd=hashpwd[0:outlen]
    elif slen>hlen:
        outlen=slen
        hashpwd=hashpwd.zfill(outlen)
    else:
        outlen=hlen
    xorvalue=int(hexshare, 16) ^ int(hashpwd, 16) # convert to integers and xor 
    paddedresult='{:x}'.format(xorvalue)          # convert back to hex
    paddedresult=paddedresult.zfill(outlen)       # pad left
    result=words[0]+"-"+paddedresult              # put index back
    return result

def pwds_shares_to_secret(kpwds,kinds,diffs):
    '''
        take k passwords, indices of those, and the "public" shares and 
        recover shamir secret
    '''
    shares=[]
    for i in range(0,len(kpwds)):
        shares.append(pxor(kpwds[i],diffs[kinds[i]]))
    secret=sss.SecretSharer.recover_secret(shares)
    return secret

#with open('json\level1.json', 'r') as f:
#    ball= json.load(f)
# modified from https://www.quickprogrammingtips.com/python/aes-256-encryption-and-decryption-in-python.html
BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def decrypt(enc, password):
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(password, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(enc[16:]))
    return decrypted

sumOfk=0
sumOfn=0
sumOfc=0
success=0

for i in range(1,11):

    jsonFile = open("json\\level"+str(i)+".json","r")
    jsonStr = jsonFile.read()
    ball = jsonpickle.decode(jsonStr)	
    jsonFile.close()
    
    ciphertext=ball["ciphertext"]
    ciphertext=str([x.encode('utf-8') for x in ciphertext])
    hashes=ball["hashes"]
    hashes=[x.encode('utf-8') for x in hashes]
    shares=ball["shares"]
    shares=[x.encode('utf-8') for x in shares]
    words=[]
    kinds=[]
    #def retrieve():
    file2 = open("potfiles\\level"+str(i)+".potfile")
    broken=file2.readlines()      

    for entry in broken:
        split = entry.strip().split(':')            
        hash = split[0]
        word = split[1]
        if len(split)>2:
            for x in range(2,len(split)):
                word=word+":"+split[x]
        words.append(word)
        kinds.append(hashes.index(hash))
        levelsecret=pwds_shares_to_secret(words,kinds,shares)
        #print(levelsecret)
        try:    
            decrypted = decrypt(ciphertext, levelsecret.zfill(32).decode('hex'))
            newball=jsonpickle.decode(bytes.decode(decrypted))
            success=1
            n=int(len(hashes))
            sumOfn+=n
            k=int(len(words))
            sumOfk+=k
            c=int(len(broken))
            sumOfc+=c
            perc=round((k/n)*100,2)
            cPerc=round((c/n)*100,2)
            print("level={},n={},k={},cracked={},k%={},cracked%={}, secret={}".format(i,n,k,c,perc,cPerc,levelsecret))
            break
        except:
            continue
    file2.close()

print "Total n", sumOfn
print "Total k", sumOfk
print "Total cracked", sumOfc
print "Overall k%", round(sumOfk/sumOfn*100)
print "Overall cracked%", round(sumOfc/sumOfn*100)

if success==0:
    n=int(len(hashes))
    c=int(len(broken))
    cPerc=round((c/n)*100,2)
    print("level={},n={},k=?,cracked={},k%=?,cracked%={}".format(i,n,c,cPerc))

"""
def encrypt(raw, key):
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

print(bytes.decode(decrypted))
csname="Complete"+".json"
path=os.path.join("json\\",csname)
with open(path,"w") as tmpf:
    tmpf.write(decrypted+"\n")
tmpf.close()

new_ciphertext=newball["ciphertext"]
#new_ciphertext=str([x.encode('utf-8') for x in new_ciphertext])
csname="level10"+".ciphertext"
path=os.path.join("ciphertext\\",csname)
with open(path,"w") as tmpf: 
    tmpf.write(new_ciphertext+"\n")
tmpf.close()
new_hashes=newball["hashes"]
csname="level10"+".hashes"
path=os.path.join("hashes\\",csname)
with open(path,"w") as tmpf:
    for hash in new_hashes:
        tmpf.write(hash+"\n")
tmpf.close()

new_shares=newball["shares"]
csname="level10"+".shares"
path=os.path.join("shares\\",csname)
with open(path,"w") as tmpf:
    for share in new_shares:
        tmpf.write(share+"\n")
tmpf.close()
"""