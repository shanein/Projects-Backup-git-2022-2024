package com.example.myapplication

import com.google.firebase.database.FirebaseDatabase

object FirebaseUtils {

    private const val DATABASE_URL = "https://dev-800-default-rtdb.europe-west1.firebasedatabase.app"

    val databaseInstance: FirebaseDatabase
        get() = FirebaseDatabase.getInstance(DATABASE_URL)

}