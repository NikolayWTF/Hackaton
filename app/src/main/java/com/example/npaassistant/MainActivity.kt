package com.example.npaassistant

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import com.example.npaassistant.databinding.ActivityMainBinding
import com.google.firebase.database.ktx.database
import com.google.firebase.ktx.Firebase

class MainActivity : AppCompatActivity() {
    lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val database = Firebase.database
        val myRef = database.getReference("Documents")

        binding.bInput.setOnClickListener {
            val document = binding.inputNPA.text
            myRef.setValue(document.toString())
            val intent = Intent(this@MainActivity, OutputActivity::class.java)
            startActivity(intent)
        }
    }
}