package com.example.circular.ufrpe.circularufrpe

import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.widget.ProgressBar
import android.widget.TextView

import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.SupportMapFragment
import com.google.android.gms.maps.model.LatLng
import com.google.android.gms.maps.model.MarkerOptions

class HomeActivity : AppCompatActivity(), OnMapReadyCallback {

    private lateinit var mMap: GoogleMap
    private lateinit var txt_posicao: TextView
    private lateinit var bar_lotacao : ProgressBar

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_home)
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        val mapFragment = supportFragmentManager
                .findFragmentById(R.id.fragmento_mapa) as SupportMapFragment
        txt_posicao = findViewById(R.id.home_txt_posicao_atual)
        bar_lotacao = findViewById(R.id.home_lotacao_bar)
        mapFragment.getMapAsync(this)
    }

    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    override fun onMapReady(googleMap: GoogleMap) {
        mMap = googleMap
        mMap.uiSettings.isScrollGesturesEnabled = false

        // Marcador ufrpe e move a câmera
        val ufrpe = LatLng(-8.015197, -34.949584)
        //mMap.addMarker(MarkerOptions().position(ufrpe).title("Marcador Centro UFRPE"))
        mMap.moveCamera(CameraUpdateFactory.newLatLng(ufrpe))

        //Travar zoom
        mMap.setMaxZoomPreference(15.0f)
        mMap.setMinZoomPreference(15.0f)
    }
}
