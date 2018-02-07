package com.br.lotacao;


import retrofit2.Call;
import retrofit2.http.GET;

public interface LotacaoService {

    @GET("lotacao")
    Call<String> getUltimo();
}