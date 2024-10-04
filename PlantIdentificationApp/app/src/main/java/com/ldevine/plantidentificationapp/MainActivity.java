    package com.ldevine.plantidentificationapp;

import android.net.Uri;
import android.os.Bundle;

import androidx.activity.EdgeToEdge;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import android.util.Log;
import android.widget.ImageView;
import android.widget.Button;
import android.content.Intent;
import android.widget.TextView;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class MainActivity extends AppCompatActivity {
    ExecutorService executorService;
    ImageView ivPlant;
    Button btnTakePhoto;
    Button btnIdentifyPlant;
    TextView tvPlantName;
    Uri plantToIdentify;
    String SERVER_IP = "192.168.0.50";
    int SERVER_PORT = 2222;
    String IDENTIFY = "!IDENTIFY";
    int BUFFER_SIZE = 1024;

    private final ActivityResultLauncher<Intent> startForResult =
            registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
                if (result.getResultCode() == RESULT_OK) {
                    Intent data = result.getData();
                    if (data != null)
                    {
                        plantToIdentify = data.getData();
                        if (plantToIdentify != null) {
                            ivPlant.setImageURI(plantToIdentify);
                        }
                    }
                }
            });

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        executorService = Executors.newSingleThreadExecutor();

        ivPlant = findViewById(R.id.ivPlant);

        btnTakePhoto = findViewById(R.id.btnTakePhoto);
        btnTakePhoto.setOnClickListener(v -> getPicture());

        btnIdentifyPlant = findViewById(R.id.btnIdentifyPlant);
        btnIdentifyPlant.setOnClickListener(v -> executorService.execute(() -> {
            String plantName = identifyPlant(plantToIdentify);
            runOnUiThread(() -> tvPlantName.setText(plantName));
        }));

        tvPlantName = findViewById(R.id.tvPlantName);
    }

    private void getPicture() {
        Intent intent = new Intent();
        intent.setType("image/*");
        intent.setAction(Intent.ACTION_GET_CONTENT);
        startForResult.launch(intent);
    }

    private String identifyPlant(Uri image) {
        try {
            Socket client = new Socket(SERVER_IP, SERVER_PORT);
            OutputStream binOut = client.getOutputStream();
            PrintWriter textOut = new PrintWriter(new OutputStreamWriter(binOut), true);
            InputStream in = client.getInputStream();
            BufferedReader textIn = new BufferedReader(new InputStreamReader(client.getInputStream()));
            textOut.println(IDENTIFY);
            sendPlant(image, binOut, in);
            return textIn.readLine();
        } catch (Exception e) {
            return e.toString();
        }
    }

    private void sendPlant(Uri image, OutputStream out, InputStream in) throws IOException {
        InputStream imageStream = getContentResolver().openInputStream(image);
        byte[] outputBuffer = new byte[BUFFER_SIZE];
        while (true) {
            int message = in.read();
            if (message == -1 || (char) message != '!')
            {
                return;
            }
            int length = imageStream.read(outputBuffer);
            if (length == -1) {
                return;
            }
            out.write(outputBuffer, 0, length);
        }
    }
}