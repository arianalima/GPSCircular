package com.example.circular.ufrpe.circularufrpe

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

private val IP_Bernardo = ""
private val IP_Ariana = "192.168.48.1"
private val IP = IP_Ariana

class RetrofitInitializer {
    private val retrofit = Retrofit.Builder()
                .baseUrl("http://" + IP + ":5001")
                .addConverterFactory(GsonConverterFactory.create())
                .build()

    fun lotacaoService() = retrofit.create(LotacaoService::class.java)
}