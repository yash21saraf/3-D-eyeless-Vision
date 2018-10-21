/* Copyright 2013 Foxdog Studios Ltd
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.example.saraf.eyes ;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.URL;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Locale;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.SharedPreferences.OnSharedPreferenceChangeListener;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.PowerManager;
import android.os.PowerManager.WakeLock;
import android.preference.PreferenceManager;
import android.speech.RecognizerIntent;
import android.speech.tts.TextToSpeech;
import android.support.v7.app.AppCompatActivity;
import android.text.format.Formatter;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import com.google.vr.sdk.audio.GvrAudioEngine;
import com.google.vr.sdk.base.GvrActivity;

import org.apache.http.conn.util.InetAddressUtils;
import org.json.JSONObject;

import javax.net.ssl.HttpsURLConnection;

import static android.content.ContentValues.TAG;

public final class StreamCameraActivity extends GvrActivity

{
    protected static final int RESULT_SPEECH = 1;

    private ImageButton btnSpeak;
    private TextView txtText;
    private String alpha ;
    private String alpha1 = "AAAA" ;
    private String alpha2 ;
    private String senderr ;
    public  String recognizedtext="";

///////////////////////////////////////////////////////////////////////////

    public float[] modelPosition;

    private static String OBJECT_SOUND_FILE = "Welcome to visual assistant.mp3";

    private GvrAudioEngine gvrAudioEngine;
    private volatile int sourceId = GvrAudioEngine.INVALID_ID;

    TextToSpeech t1;

    @Override
    protected void onCreate(final Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        t1=new TextToSpeech(getApplicationContext(), new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if(status != TextToSpeech.ERROR) {
                    t1.setLanguage(Locale.UK);
                }
            }
        });
        alpha2 = getLocalIpAddress() ;
        alpha2 = alpha2 + "." ;
        Toast.makeText(getApplicationContext(), alpha2, Toast.LENGTH_LONG).show();


        txtText = (TextView) findViewById(R.id.txtText);
        btnSpeak = (ImageButton) findViewById(R.id.btnSpeak);

        //onClick Method definition
        btnSpeak.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {

                Intent intent = new Intent(
                        RecognizerIntent.ACTION_RECOGNIZE_SPEECH);

                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, "en-US");
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, "en-US");
                try {
                    startActivityForResult(intent, RESULT_SPEECH);
                    txtText.setText("");
                } catch (ActivityNotFoundException a) {
                    Toast t = Toast.makeText(getApplicationContext(),
                            "Opps! Your device doesn't support Speech to Text",
                            Toast.LENGTH_SHORT);
                    t.show();
                }
            }
        });
        HashMap<String, String> myHashRender = new HashMap();
        modelPosition = new float[]{0.0f, 0.0f, 0.0f};

        gvrAudioEngine = new GvrAudioEngine(this, GvrAudioEngine.RenderingMode.BINAURAL_HIGH_QUALITY);


        ststereo("Welcome to visual assistant", 0.0f,0.0f);
        try {
            Thread.sleep(2000);

        } catch (InterruptedException ie) {
            ie.printStackTrace();
        }
        ststereo("right right right", 0.1f,0.0f);
        try {
            Thread.sleep(2000);

        } catch (InterruptedException ie) {
            ie.printStackTrace();
        }

        ststereo("left left left", -0.1f,0.0f);

        new SendPostRequest().execute();
    } // onCreate(Bundle)


    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        switch (requestCode) {
            case RESULT_SPEECH: {
                if (resultCode == RESULT_OK && null != data) {

                    ArrayList<String> text = data
                            .getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);

                    recognizedtext=text.get(0);
                    txtText.setText(text.get(0));

                }
                break;
            }
        }
    }

    public String getLocalIpAddress(){
        try {
            for (Enumeration<NetworkInterface> en = NetworkInterface.getNetworkInterfaces();
                 en.hasMoreElements();) {
                NetworkInterface intf = en.nextElement();
                for (Enumeration<InetAddress> enumIpAddr = intf.getInetAddresses(); enumIpAddr.hasMoreElements();) {
                    InetAddress inetAddress = enumIpAddr.nextElement();
                    if (!inetAddress.isLoopbackAddress() && inetAddress instanceof Inet4Address) {
                        return inetAddress.getHostAddress();
                    }
                }
            }
        } catch (Exception ex) {
            Log.e("IP Address", ex.toString());
        }
        return null;
    }

    public void ststereo(String objsoundfile, float a, float b){
        modelPosition[0] = a;
        modelPosition[2] = b;
        OBJECT_SOUND_FILE = objsoundfile + ".mp3" ;
        gvrAudioEngine.preloadSoundFile(OBJECT_SOUND_FILE);
        sourceId = gvrAudioEngine.createSoundObject(OBJECT_SOUND_FILE);
        gvrAudioEngine.setSoundObjectPosition(
                sourceId, modelPosition[0], 0.0f, modelPosition[2]);
        gvrAudioEngine.playSound(sourceId, false /* looped playback */);
    }

    public class SendPostRequest extends AsyncTask<String, Void, String> {

        protected void onPreExecute() {
        }
        protected String doInBackground(String... arg0) {
            while (true) {
                try {

                    URL url = new URL("http://192.168.0.4/object_detection/test.py"); // here is your URL path

                    JSONObject postDataParams = new JSONObject();
                    senderr = alpha2 + recognizedtext ;
                    postDataParams.put("statement", senderr);
                    // postDataParams.put("email", "abc@gmail.com");
                    Log.e("params", postDataParams.toString());

                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setReadTimeout(15000 /* milliseconds */);
                    conn.setConnectTimeout(15000 /* milliseconds */);
                    conn.setRequestMethod("POST");
                    conn.setDoInput(true);
                    conn.setDoOutput(true);

                    OutputStream os = conn.getOutputStream();
                    BufferedWriter writer = new BufferedWriter(
                            new OutputStreamWriter(os, "UTF-8"));
                    writer.write(getPostDataString(postDataParams));

                    writer.flush();
                    writer.close();
                    os.close();
                    Log.e("hi", "RAJEEV");
                    int responseCode = conn.getResponseCode();


                    if (responseCode == HttpsURLConnection.HTTP_OK) {

                        BufferedReader in = new BufferedReader(new
                                InputStreamReader(
                                conn.getInputStream()));

                        StringBuffer sb = new StringBuffer("");
                        String line = "";

                        while ((line = in.readLine()) != null) {

                            sb.append(line);
                            break;
                        }

                        in.close();
                        alpha1 = sb.toString();
                        Log.e(TAG, alpha1 );

                    }

                    else {
                        alpha = new String("false : " + responseCode);
                        Log.e(TAG, alpha);
                    }

                } catch (Exception e) {
                    alpha = new String("Exception: " + e.getMessage());
                    Log.e(TAG, alpha );
                }

                if (!alpha1.equals("AAAA")) {

                    recognizedtext = "";
                    Log.e(TAG, "run: Relevant data recieved" );
                    String array1[]= alpha1.split(";");
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            txtText.setText(alpha1);

                        }
                    });
                    if(array1[0].equals("Follow"))
                    {
                        float aa = Float.parseFloat(array1[2]);
                        float bb = Float.parseFloat(array1[3]);
                        ststereo(array1[1],aa,bb ) ;
                    }
                    else if(array1[0].equals("Search"))
                    {
                        float aa = Float.parseFloat(array1[2]);
                        float bb = Float.parseFloat(array1[3]);
                        ststereo(array1[1],aa,bb ) ;
                    }
                    else if(array1[0].equals("Overview"))
                    {
                        float aa = Float.parseFloat(array1[2]);
                        float bb = Float.parseFloat(array1[3]);
                        ststereo(array1[1],aa,bb ) ;

                    }
                    else if(array1[0].equals("Read"))
                    {

                    }
                    if(array1[0].equals("Date Time"))
                    {

                        ststereo(array1[1],0.0f,0.0f ) ;
                        try {
                            Thread.sleep(500);

                        } catch (InterruptedException ie) {
                            ie.printStackTrace();
                        }
                        ststereo(array1[2],0.0f,0.0f ) ;
                        try {
                            Thread.sleep(500);

                        } catch (InterruptedException ie) {
                            ie.printStackTrace();
                        }
                        ststereo(array1[3],0.0f,0.0f ) ;
                        try {
                            Thread.sleep(500);

                        } catch (InterruptedException ie) {
                            ie.printStackTrace();
                        }
                        ststereo("hours",0.0f,0.0f ) ;
                        try {
                            Thread.sleep(500);

                        } catch (InterruptedException ie) {
                            ie.printStackTrace();
                        }
                        ststereo(array1[4],0.0f,0.0f ) ;
                        try {
                            Thread.sleep(500);

                        } catch (InterruptedException ie) {
                            ie.printStackTrace();
                        }
                        ststereo("minutes",0.0f,0.0f ) ;

                    }

                    if(array1[0].equals("Currency"))
                    {
                        float aa = Float.parseFloat(array1[2]);
                        float bb = Float.parseFloat(array1[3]);
                        ststereo(array1[1],aa,bb ) ;
                        try {
                            Thread.sleep(700);

                        } catch (InterruptedException ie) {
                            ie.printStackTrace();
                        }
                    }
                    alpha1 = "AAAA";


                }
            }
        }
        /*@Override
        protected void onPostExecute(String result) {
            Toast.makeText(getApplicationContext(), result,
                    Toast.LENGTH_LONG).show();

        }*/
    }

    public String getPostDataString(JSONObject params) throws Exception {

        StringBuilder result = new StringBuilder();
        boolean first = true;

        Iterator<String> itr = params.keys();

        while (itr.hasNext()) {

            String key = itr.next();
            Object value = params.get(key);

            if (first)
                first = false;
            else
                result.append("&");

            result.append(URLEncoder.encode(key, "UTF-8"));
            result.append("=");
            result.append(URLEncoder.encode(value.toString(), "UTF-8"));

        }
        return result.toString();
    }



    @Override
    protected void onResume()
    {
        super.onResume();
        gvrAudioEngine.resume();
    } // onResume()

    @Override
    protected void onPause()
    {
        if(t1 !=null){
            t1.stop();
            t1.shutdown();
        }
        gvrAudioEngine.pause();
        super.onPause();
    } // onPause()

} // class StreamCameraActivity

