package com.example.stptest

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ButtonDefaults.buttonColors
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.stptest.ui.theme.AppTheme


class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            AppTheme {
                // A surface container using the 'background' color from the theme
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    WelcomeContent("AppName")
                }
            }
        }
    }
}

@Composable
fun WelcomeContent(name: String, modifier: Modifier = Modifier) {
    val image = painterResource(R.drawable.welcome_image)
    var username by remember { mutableStateOf("") }

    Column(
        modifier = modifier,
        verticalArrangement = Arrangement.spacedBy(5.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Image(
            painter = image,
            contentDescription = null,
            contentScale = ContentScale.Fit,
            modifier = Modifier
                .padding(start = 20.dp, end = 20.dp, top = 20.dp, bottom = 0.dp)
                .size(400.dp) // Adjust the size as needed
        )

        Text(
            text = "Make things easier with $name",
            modifier = Modifier
                .padding(horizontal = 50.dp)
                .align(Alignment.CenterHorizontally),
            textAlign = TextAlign.Center,
            fontSize = 30.sp,
            lineHeight = 40.sp
        )

        Text(
            text = "$name is a free public transport subscription manager",
            modifier = Modifier
                .padding(horizontal = 80.dp)
                .align(Alignment.CenterHorizontally),
            textAlign = TextAlign.Center,
            fontSize = 15.sp,
            lineHeight = 20.sp
        )

        // "Sign Up" Button
        Button(
            onClick = {
                // Handle the Sign Up button click action
            },
            colors = buttonColors(Color(0xFFFF4967)),
            modifier = Modifier
                .padding(top = 50.dp)
        ) {
            Text(text = "Sign Up", color = Color.White, fontSize = 15.sp)
        }

        TextButton(
            onClick = {
                // Handle the Text button click action
            },
            modifier = Modifier
                .padding(start = 20.dp, end = 20.dp)
        ) {
            Text(text = "Log in", color = Color(0xFFFF4967), fontSize = 15.sp)
        }

    }
}

@Preview(showBackground = true, showSystemUi = true)
@Composable
fun MainPagePreview() {
    AppTheme {
        WelcomeContent(name = "AppName")
    }
}