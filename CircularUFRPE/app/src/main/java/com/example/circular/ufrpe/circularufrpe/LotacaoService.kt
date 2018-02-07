package com.example.circular.ufrpe.circularufrpe

import retrofit2.http.GET
import retrofit2.Call

interface LotacaoService {

    @GET("/circular/get/lotacao")
    fun getLotacao(): Call<Lotacao>
}