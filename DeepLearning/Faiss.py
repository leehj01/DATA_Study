# 임의로 데이터 값 넣기
index_ids = np.array(list(range(1000,1100))) # 인덱스
text_vector = np.random.rand(100,1024).astype('float32') 
print('text_vector shape : ', text_vector.shape)

res = faiss.StandardGpuResources() # 단일 gpu 사용 

# 값을 코사인 유사도를 해주기 위해서 normalize 해줌 
faiss.normalize_L2(text_vector)

# 백터의 차원을 알려주는 역할을 함 # build the index - cpu로 빌드해줌 
cos_index = faiss.IndexFlatIP(text_vector.shape[1])
print(cos_index.is_trained)

# 인덱스를 매핑해줌
cos_index = faiss.IndexIDMap2(cos_index)

# gpu index가 되게 함 
gpu_index_flat = faiss.index_cpu_to_gpu(res, 0, cos_index)

# add 함수로 vector 값을 넣어주기  add vectors to the index
# 벡터와 인덱스를 넣어줌
gpu_index_flat.add_with_ids(text_vector, index_ids)
# gpu_index_flat.add(text_vector) 
print(gpu_index_flat.ntotal)

# search 함수로 유사한 인덱스를 찾아오기
k  = 51 # knn 에서 가져올 갯수 - shoppe 에서는 51개를 찾아오기 ( 1개는 자기 자신 )
distances, indices = gpu_index_flat.search(text_vector[2].reshape(1,-1), k)

dic = {}
for idx, (id_, v) in enumerate(zip(index_ids,temp )):
    distances, indices = gpu_index_flat.search(text_vector[idx].reshape(1,-1), k)
    temp_distances = distances.tolist()
    temp_distances = list(filter(lambda x : x > 0.5, temp_distances[0]))  # threshold 0.5이상
    distances = np.array(temp_distances)

    cos_list = []
    for j in range(50):
        cos_list.append((indices[0][j], distances[j]))

    dic[id_] = cos_list


# 2. min 도 설정 ( concat 에서만 존재 ) : 각 아이템은 최소 본인포함 최소 2개를 가지고 있어서, min2 를 가지게 함.  min2 가 되도록 보장하도록 함. thresholding 을 하더라도 2개 이상 가져오게 함 
