package com.example.npaassistant

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.npaassistant.databinding.ActivityOutputBinding
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.ValueEventListener
import com.google.firebase.database.ktx.database
import com.google.firebase.ktx.Firebase

class OutputActivity : AppCompatActivity() {

    lateinit var binding: ActivityOutputBinding
    lateinit var adapter: OutputRCAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityOutputBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val database = Firebase.database
        val myRef = database.getReference("Python")

        myRef.addValueEventListener(object: ValueEventListener {
            override fun onDataChange(dataSnapshot: DataSnapshot) {
                val list = ArrayList<OutputRC>()
                var i = 1
                for (postSnapshot in dataSnapshot.children){
                    val value = postSnapshot.value.toString()
                    val classNpa = OutputRC(i.toString(), value)
                    list.add(classNpa)
                    i += 1
                }
                adapter.submitList(list)
            }
            override fun onCancelled(error: DatabaseError) {}
        })
        init()
    }
    private fun init(){
        binding.apply {
            adapter = OutputRCAdapter()
            recyclerView.layoutManager = LinearLayoutManager(this@OutputActivity)
            recyclerView.adapter = adapter
        }
    }
}