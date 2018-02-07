package com.br.lotacao;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;


public class MainActivity extends AppCompatActivity {
    private TextView txtlotacao;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        txtlotacao = (TextView) findViewById(R.id.txt_lotacao);

        Button button = findViewById(R.id.btn_atualizar);
        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                getLotacao();
            }
        });

    }

    public void getLotacao(){

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://192.168.48.1:5001/circular/get/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        LotacaoService localService = retrofit.create(LotacaoService.class);


        Call<String> listaCall = localService.getUltimo();

        listaCall.enqueue(new Callback<String>() {
            @Override
            public void onResponse(Call<String> call, Response<String> response) {
                if(response.isSuccessful()){
                    String  resposta = response.body();
                    if(!resposta.isEmpty()){
//                        Toast.makeText(getApplicationContext(),resposta,Toast.LENGTH_LONG).show();
                        txtlotacao.setText(resposta);
                    }else{
                        Toast.makeText(getApplicationContext(),"" + response.message() ,Toast.LENGTH_LONG).show();
                    }
                }else {
                    Toast.makeText(getApplicationContext(),"" + response.code() ,Toast.LENGTH_LONG).show();
                }
            }

            @Override
            public void onFailure(Call<String> call, Throwable t) {
                Toast.makeText(getApplicationContext(),t.getMessage(),Toast.LENGTH_LONG).show();
            }
        });
    }
}
