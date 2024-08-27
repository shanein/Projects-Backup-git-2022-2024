package com.example.myapplication

import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.bumptech.glide.Glide
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.database.*
import com.google.firebase.storage.FirebaseStorage
import com.google.firebase.storage.StorageReference
import com.google.gson.Gson
import java.net.URLDecoder

class ImageDetailActivity : AppCompatActivity() {

    private lateinit var storageRef: StorageReference

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_image_detail)

        val photoJson = intent.getStringExtra(EXTRA_IMAGE_URL)
        if (photoJson != null) {

            //Récuperation du proprietaire de la photo
            val userPhotoId = intent.getStringExtra(EXTRA_IMAGE_USER_ID)
            if (userPhotoId != null) {
                val firebaseRef = FirebaseUtils.databaseInstance.getReference("users/$userPhotoId")
                Log.d("Photo id TESSSSSSSST", userPhotoId.toString())

                firebaseRef.addListenerForSingleValueEvent(object : ValueEventListener {
                    override fun onDataChange(dataSnapshot: DataSnapshot) {
                        val userFirstName = dataSnapshot.child("firstName").value?.toString()
                        val userLastName = dataSnapshot.child("lastName").value?.toString()
                        val userEmail = dataSnapshot.child("email").value?.toString()

                        // Mise à jour du texte dans votre TextView
                        val textViewEmail = findViewById<TextView>(R.id.textview_email)
                        val textViewName = findViewById<TextView>(R.id.textview_name)

                        textViewEmail.text = "Owner's Email : $userEmail"
                        textViewName.text = "Owner : $userFirstName $userLastName"
                    }

                    override fun onCancelled(error: DatabaseError) {
                    }
                })
            }

            val imageView: ImageView = findViewById(R.id.image_view)

            val photo = Gson().fromJson(photoJson, ListFragment.Photo::class.java)
            Log.d("ImageDetailActivity", "Photo: $photo")
            Glide.with(this)
                .load(photo.url)
                .into(imageView)


            // Récupération de l'e-mail de l'utilisateur connecté
            val userEmail = FirebaseAuth.getInstance().currentUser?.email
            Log.d("Email", userEmail.toString())



            // Recherche de l'ID de l'utilisateur dans la base de données en utilisant son e-mail
            FirebaseUtils.databaseInstance.getReference("users")
                .orderByChild("email")
                .equalTo(userEmail)
                .addListenerForSingleValueEvent(object : ValueEventListener {
                    override fun onDataChange(snapshot: DataSnapshot) {
                        if (snapshot.exists()) {
                            // L'utilisateur existe dans la base de données
                            val userIdbdd = snapshot.children.first().key // Récupération de l'ID de l'utilisateur
                            // Utiliser userId pour récupérer la référence de l'image dans la base de données
                            val idPhoto = photo.id

                            val imageRef: DatabaseReference = FirebaseUtils.databaseInstance.getReference("users/$userIdbdd/photos/$idPhoto")
                            Log.d("ImageRef", imageRef.toString())


                            val userId = FirebaseAuth.getInstance().currentUser?.uid
                            val imageName = URLDecoder.decode(photo.url, "UTF-8").substringAfterLast("/").substringBeforeLast(".jpg").plus(".jpg")
                            // Récupération de la référence de l'image dans Firebase Storage
                            storageRef = FirebaseStorage.getInstance().getReference("images/$userId").child(imageName)
                            //lien non trouvé
                            Log.d("StorageRef image", imageName)

                            Log.d("StorageRef", storageRef.toString())

                            val shareButton: Button = findViewById(R.id.share_button)
                            val emailInput: EditText = findViewById(R.id.email_input)
                            val usersRef = FirebaseUtils.databaseInstance.getReference("users")
                            val deleteButton: Button = findViewById(R.id.delete_button)


                            imageRef.addListenerForSingleValueEvent(object : ValueEventListener {
                                override fun onDataChange(dataSnapshot: DataSnapshot) {
                                    if (dataSnapshot.exists()) {
                                        // La référence existe dans la base de données
                                        shareButton.visibility = View.VISIBLE
                                        emailInput.visibility = View.VISIBLE
                                        deleteButton.visibility = View.VISIBLE

                                        shareButton.setOnClickListener {
                                            val email = emailInput.text.toString().trim()
                                            if (email.isNotEmpty()) {
//                                    sharePhotoWithUser(userIdbdd, idPhoto, email)
                                                usersRef
                                                    .orderByChild("email")
                                                    .equalTo(email)
                                                    .addListenerForSingleValueEvent(object : ValueEventListener {
                                                        override fun onDataChange(snapshot: DataSnapshot) {
                                                            if (snapshot.exists()) {
                                                                val sharedWithUserId = snapshot.children.first().key
                                                                Log.d("Share info", "userIdbdd: $userIdbdd, idPhoto: $idPhoto, email: $email. sharedWithUserId: $sharedWithUserId")

                                                                usersRef.child("$userIdbdd/photos/$idPhoto/sharedWith/$sharedWithUserId").setValue(true)

                                                                usersRef.child("$sharedWithUserId/sharedPhotos/$idPhoto/").setValue(userIdbdd)

                                                                emailInput.text.clear()

                                                            } else {
                                                                Toast.makeText(this@ImageDetailActivity, "Error: Email User not found", Toast.LENGTH_SHORT).show()
                                                            }
                                                        }
                                                        override fun onCancelled(error: DatabaseError) {
                                                            // Gérer l'erreur

                                                        }
                                                    })
                                            } else {
                                                emailInput.error = "Email is required"
                                                return@setOnClickListener
                                            }
                                        }

                                        //         Configuration du bouton "Delete"
                                        deleteButton.setOnClickListener {
                                            // Suppression de l'image dans la base de données
                                            imageRef.removeValue()
                                                .addOnSuccessListener {
                                                    Log.d("ImageDetailActivity", "Image deleted from database")
                                                }
                                                .addOnFailureListener {
                                                    Log.e("ImageDetailActivity", "Error deleting image from database", it)
                                                }

                                            // Suppression de l'image dans Firebase Storage
                                            storageRef.delete()
                                                .addOnSuccessListener {
                                                    Log.d("ImageDetailActivity", "Image deleted from Firebase Storage")
                                                    finish() // Fermeture de l'activité après la suppression réussie de l'image
                                                }
                                                .addOnFailureListener {
                                                    Log.e("ImageDetailActivity", "Error deleting image from Firebase Storage", it)
                                                }
                                            // Créer une instance de la classe listFragment
                                            val fragment = ListFragment()

                                            // Appeler la méthode de suppression sur l'instance de la classe listFragment
                                            fragment.deletePhoto(photo)
                                        }
                                    } else {
                                        // La référence n'existe pas dans la base de données
                                        shareButton.visibility = View.GONE
                                        emailInput.visibility = View.GONE
                                        deleteButton.visibility = View.GONE
                                    }
                                }

                                override fun onCancelled(databaseError: DatabaseError) {
                                    // Une erreur s'est produite lors de la recherche de la référence dans la base de données
                                    // Gérer l'erreur en conséquence
                                }
                            })
                        }
                    }
                    override fun onCancelled(error: DatabaseError) {
                            // Gérer l'erreur
                        }
                })
            // Récupération de l'id de l'image
//
//        // Récupération de la référence de l'image dans la base de données
//        val Idphoto = photo.id
//        imageRef = FirebaseUtils.databaseInstance.getReference("users/$userId/photos/$Idphoto")
            //changer il faut recup l'id par rapport a l'email
//        Log.d("ImageRef", imageRef.toString())
        }
    }



    companion object {
        const val EXTRA_IMAGE_URL = "extra_image_res_id"
        const val EXTRA_IMAGE_USER_ID = "none"
    }

}