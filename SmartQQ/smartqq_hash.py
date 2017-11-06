#! /usr/bin/env python3

# SmartQQ数据验证时需要用到的两个哈希函数

# 检查二维码状态的hash
def hash1(qrsig) :
	e = 0
	for ch in qrsig :
		e += (e << 5) + ord(ch)
	return 2147483647 & e

# 拉取好友、群列表的哈希
def hash2(qq, ptwebqq):
    N = [0] * 4
    for T in range(len(ptwebqq)):
        N[T%4] ^= ord(ptwebqq[T])

    U, V = 'ECOK', [0] * 4
    V[0] = ((qq >> 24) & 255) ^ ord(U[0])
    V[1] = ((qq >> 16) & 255) ^ ord(U[1])
    V[2] = ((qq >>  8) & 255) ^ ord(U[2])
    V[3] = ((qq >>  0) & 255) ^ ord(U[3])

    U1 = [0] * 8
    for T in range(8):
        U1[T] = N[T >> 1] if T % 2 == 0 else V[T >> 1]

    N1, V1 = '0123456789ABCDEF', ''
    for aU1 in U1:
        V1 += N1[((aU1 >> 4) & 15)]
        V1 += N1[((aU1 >> 0) & 15)]

    return V1
