package com.example.mocparkingapp;

import android.support.annotation.NonNull;
import android.support.v4.app.FragmentActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import java.util.List;
import java.util.ArrayList;
import java.util.Objects;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import android.content.Context;
import android.graphics.Point;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.widget.RelativeLayout;

public class MapsActivity extends FragmentActivity
        implements
        OnMapReadyCallback,
        GoogleMap.OnMarkerClickListener,
        GoogleMap.InfoWindowAdapter{

    private GoogleMap mMap;

    /** Called before anything */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        assert mapFragment != null;
        mapFragment.getMapAsync(this);
    }

    /** Called on map Ready */
    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;

        // Read data from CSV
        CSVFile csvFile = new CSVFile(getResources().openRawResource(R.raw.cords));
        List<String[]> csvData = csvFile.read();

        // Define aLists for pin data
        final Marker[] markers = new Marker[csvData.size()];
        ArrayList<LatLng> cords = new ArrayList<>();
        final ArrayList<String> names = new ArrayList<>();

        // Add csv data to lists
        for(String[] d:csvData) {
            names.add(d[0]);
            cords.add(new LatLng(Double.parseDouble(d[1]), Double.parseDouble(d[2])));
        }

        // Add pins off pin data list
        int n = 0;
        for(LatLng cord : cords){
            String lot = names.get(n);
            markers[n] = mMap.addMarker(new MarkerOptions()
                    .position(cord)
                    .title(lot)
                    .icon(BitmapDescriptorFactory.fromResource(R.drawable.pin_icon_grey))
                    );
            markers[n].setAnchor((float) 0.5,(float) .5);
            n++;
        }

        // Center Camera (Center cord needs changing!)
        LatLng camCenter = new LatLng(28.031472, -81.946042);
        mMap.moveCamera(CameraUpdateFactory
                .newLatLngZoom(camCenter, 15.5f));

        // Sets a listener for user tapping a marker
        mMap.setOnMarkerClickListener(this);

        // Database
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        final DatabaseReference ref = database.getReferenceFromUrl("https://mocparkingapp.firebaseio.com/");

        ref.addValueEventListener(new ValueEventListener() {
            /** Called initially and on database change */
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                for (DataSnapshot child : dataSnapshot.getChildren()){

                    int index = names.indexOf((child.getKey()).replaceAll("_"," "));
                    Log.w(null, Integer.toString(index));
                    if(index == -1) continue;
                    String value = "" + child.child("Spaces").getValue();

                    markers[index].setSnippet("Availability: " + value);

                    if(Integer.parseInt(value) == 0){
                        markers[index].setIcon(BitmapDescriptorFactory.fromResource(R.drawable.pin_icon_grey ));}
                    else if(Integer.parseInt(value) < 3){
                        markers[index].setIcon(BitmapDescriptorFactory.fromResource(R.drawable.pin_icon_red));}
                    else if(Integer.parseInt(value) < 10){
                        markers[index].setIcon(BitmapDescriptorFactory.fromResource(R.drawable.pin_icon_orange));}
                    else{
                        markers[index].setIcon(BitmapDescriptorFactory.fromResource(R.drawable.pin_icon_green));}
                }
            }

            /** Called when database throws an error */
            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });

        // Info window hooplah]
    }

    /** Called when user clicks a marker */
    @Override
    public boolean onMarkerClick(final Marker marker) {
        marker.showInfoWindow();
        return false;// (from google) Return false to indicate that we have not consumed the event
    }

    /** Called 1st when info window is opened   *
     *  Changes how the info window looks       */
    @Override
    public View getInfoWindow(Marker marker) {
        // Use the default window layout
        return null;
    }

    /** Called 2nd when info window is opened   *
     *  Customizes the content of the window    */
    @Override
    public View getInfoContents(Marker marker) {
        View contentsView = getLayoutInflater().inflate(R.layout.custom_info_contents, null);

        TextView pinTitle = (contentsView.findViewById(R.id.title));
        pinTitle.setText(marker.getTitle());

        TextView tvSnippet = (contentsView.findViewById(R.id.snippet));
        tvSnippet.setText(marker.getSnippet());

        return contentsView;
    }
}