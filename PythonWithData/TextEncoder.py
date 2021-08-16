class TextEncoder(torch.nn.Module):
    def __init__(self):
        max_length = 128
        # 구현 모델에서는 large 지만, 일단 base 로 시도 
        model_name = 'xlm-roberta-base' # 허깅페이스에 있는 모델 
        config = XLMRobertaConfig.from_pretrained(model_name)
        tokenizer = XLMRobertaTokenizer.from_pretrained(model_name) 
        XLMRmodel = XLMRobertaModel.from_pretrained(model_name,  output_hidden_states = False)  # 마지막 단만 부르기.  # 미리 학습된 모델(가중치) 불러오기

        self.embedding_layer = XLMRmodel
        
        
        self.pooling_layer = torch.nn.AvgPool1d(max_length, stride=None, padding=0, ceil_mode=False, count_include_pad=True)
        self.batchnorm = torch.nn.BatchNorm1d(max_length)
        
    # overiding
    def forward(x):  # x: input tensor
        ## tokens_tensor0, segments_tensors0 차이점 알아보기
        x = self.embedding_layer(x)  # 토큰화 작업을 마친 벡터를 넣으면 - embedding in : (batch_size , max_token_legth ) out : ( batchsize, max_token_lengh, hidden_vector)
        x = self.pooling_layer(x) # pooling  in : ( b, max_token_lengh hidden_vector) ex, [1, 512, 768]  out : (b , max_token_lengh )
        
        return x 
