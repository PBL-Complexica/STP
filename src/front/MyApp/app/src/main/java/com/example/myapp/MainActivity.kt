package com.example.myapp
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.EditText
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private lateinit var editText: EditText
    private lateinit var sendButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        editText = findViewById(R.id.editText)
        sendButton = findViewById(R.id.sendButton)

        sendButton.setOnClickListener {
            // Get the text from the EditText
            val inputData = editText.text.toString()

            // Send the data to the backend (you'll need to implement this)
            sendDataToBackend(inputData)
        }
    }
    private fun sendDataToBackend(data: String) {
        // Implement your logic to send data to the backend here
        // You can use libraries like Retrofit or Volley for network requests
        // This is where you would make an HTTP request to your backend server
        // and handle the response.
    }
}