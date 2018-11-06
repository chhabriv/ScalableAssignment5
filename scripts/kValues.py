# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 19:40:23 2018

@author: viren
"""
from __future__ import division
# for JSON output
import jsonpickle # install via  "$ sudo pip install -U jsonpickle"
# for hashing passwords
from hashlib import sha256
import secretsharing as sss


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
sumOfk=0
sumOfn=0
sumOfc=0
for i in range(1,10):
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
    # Create dict from hashes to shares
    prevSecret=""
    success=0
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
        if prevSecret==levelsecret:
            success=1
            n=int(len(hashes))
            sumOfn+=n
            k=int(len(words)-1)
            sumOfk+=k
            c=int(len(broken))
            sumOfc+=c
            perc=round((k/n)*100,2)
            cPerc=round((c/n)*100,2)
            print("level={},n={},k={},cracked={},k%={},cracked%={}".format(i,n,k,c,perc,cPerc))
            break
        prevSecret=levelsecret
            #share in inferno.values:
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