package com.example.myapplication

import android.Manifest
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.Toast
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.core.content.FileProvider
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.myapplication.databinding.FragmentListSharedBinding
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import java.io.File
import java.text.SimpleDateFormat
import java.util.*


import com.google.firebase.storage.FirebaseStorage
import com.google.firebase.database.ValueEventListener
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.tasks.await
import kotlinx.coroutines.withContext


class ListFragmentShared : Fragment() {

    private lateinit var recyclerView: RecyclerView // RecyclerView pour afficher les images

    private var _binding: FragmentListSharedBinding? = null
    private val binding get() = _binding!!

    private var pictureIV  : ImageView? = null
    private lateinit var photoFile: File
    private lateinit var currentPhotoPath: String
    private val PICTURE_FROM_CAMERA: Int = 1

//    private val urls = ArrayList<String>()
    private val photos = ArrayList<ListFragment.Photo>()
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        _binding = FragmentListSharedBinding.inflate(inflater, container, false)

        initView()


        recyclerView = binding.recyclerView
        recyclerView.layoutManager = GridLayoutManager(requireContext(), 3) // Afficher les images en grille 3x3

        initRecyclerView()

        val PicturesButton = binding.myPictures
        PicturesButton.setOnClickListener {
            // Code pour rediriger vers la page "sharedpictures"
            // Utilisez ici l'intent ou la méthode de navigation appropriée en fonction de votre architecture d'application
            findNavController().navigate(R.id.action_ListFragmentShared_to_ListFragment)
        }

        return binding.root
    }
    //List grid des phtos
    private fun initRecyclerView() {
        val email = FirebaseAuth.getInstance().currentUser?.email
        val usersRef = FirebaseUtils.databaseInstance.getReference("users")
        val storage = FirebaseStorage.getInstance()
        val userId = FirebaseAuth.getInstance().currentUser?.uid
        val storageRef = storage.reference.child("images/$userId/")

        photos.clear()
        usersRef.orderByChild("email").equalTo(email).addListenerForSingleValueEvent(object : ValueEventListener {
            override fun onDataChange(snapshot: DataSnapshot) {
                if (snapshot.exists()) {
                    val userSharedId = snapshot.children.first().key.toString() // Récupère l'identifiant de l'utilisateur partagé
                    val photosSharedRef = FirebaseUtils.databaseInstance.getReference("users/$userSharedId/sharedPhotos") // Référence de la liste des photos partagées
                    Log.d("photos ref", photosSharedRef.toString())

                    photosSharedRef.addListenerForSingleValueEvent(object : ValueEventListener {
                        override fun onDataChange(snapshot: DataSnapshot) {
                            // ...
                            for (photoSnapshot in snapshot.children) {
                                val photoId = photoSnapshot.key // Récupère l'identifiant de la photo
                                val userID = photoSnapshot.getValue() // Récupère l'identifiant de l'utilisateur de la photo

                                val photoRef = FirebaseUtils.databaseInstance.getReference("users/$userID/photos/$photoId")
                                Log.d("photoRef", photoRef.toString())
                                photoRef.addListenerForSingleValueEvent(object : ValueEventListener {
                                    override fun onDataChange(dataSnapshot: DataSnapshot) {
                                        val photo = dataSnapshot.getValue(ListFragment.Photo::class.java)
                                        photo?.let {
                                            val url = it.url
                                            val photoObject = ListFragment.Photo(photoId!!, url)
                                            photos.add(photoObject)
                                        }
                                        // Déplacez le code pour alimenter l'adaptateur ici, après la boucle for
                                        val adapter = ImageAdapter(requireContext(), photos, userID.toString())
                                        recyclerView.adapter = adapter
                                    }

                                    override fun onCancelled(databaseError: DatabaseError) {
                                        // ...
                                    }
                                })
                            }
                        }

                        override fun onCancelled(error: DatabaseError) {
                            // ...
                        }
                    })
                } else {
                    // L'utilisateur n'a pas été trouvé dans la base de données Firebase
                }
            }

            override fun onCancelled(error: DatabaseError) {
                // Une erreur s'est produite lors de la recherche de l'utilisateur dans la base de données Firebase
            }
        })
    }


    //Btn Prise de photo

//    data class Photo(
//        val id: String = "",
//        val url: String = "",
//        val sharedWith: HashMap<String, Boolean> = HashMap()
//    )

    private fun initView() {
        pictureIV = binding.picture
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        try {
            if (resultCode == Activity.RESULT_OK) {
                val uri = FileProvider.getUriForFile(requireContext(), "com.example.myapplication.fileprovider", photoFile)
                pictureIV!!.setImageURI(uri)

                val storage = FirebaseStorage.getInstance()
                val storageRef = storage.reference
                val email = FirebaseAuth.getInstance().currentUser?.email
                val userId = FirebaseAuth.getInstance().currentUser?.uid
                val imageRef = storageRef.child("images/$userId/${photoFile.name}")
                val uploadTask = imageRef.putFile(uri)

                val usersRef = FirebaseUtils.databaseInstance.getReference("users")

                usersRef.orderByChild("email").equalTo(email).addListenerForSingleValueEvent(object : ValueEventListener {
                    override fun onDataChange(snapshot: DataSnapshot) {
                        if (snapshot.exists()) {
                            val userId = snapshot.children.first().key.toString()
                            val photosRef = FirebaseUtils.databaseInstance.getReference("users/$userId/photos")

                            CoroutineScope(Dispatchers.IO).launch {
                                uploadTask.await()

                                val photoUrl = imageRef.downloadUrl.await().toString()
                                val photoId = photosRef.push().key
                                val photo = ListFragment.Photo(photoId!!, photoUrl, HashMap())
                                photosRef.child(photoId ?: "").setValue(photo)

                                withContext(Dispatchers.Main) {
                                    photos.add(photo)
                                    recyclerView.adapter?.notifyDataSetChanged()
                                }
                            }
                        } else {
                            // L'utilisateur n'a pas été trouvé dans la base de données Firebase
                            Toast.makeText(context, "Utilisateur introuvable", Toast.LENGTH_SHORT).show()
                        }
                    }

                    override fun onCancelled(error: DatabaseError) {
                        // Une erreur s'est produite lors de la recherche de l'utilisateur dans la base de données Firebase
                        Toast.makeText(context, "Erreur : ${error.message}", Toast.LENGTH_SHORT).show()
                    }
                })
            } else {
                super.onActivityResult(requestCode, resultCode, data)
            }
        } catch (e: Exception) {
            Toast.makeText(requireContext(), "Erreur: ${e.message}", Toast.LENGTH_SHORT).show()
        }
    }

//    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
//        try {
//            if (resultCode == Activity.RESULT_OK) {
//                val uri = FileProvider.getUriForFile(requireContext(), "com.example.myapplication.fileprovider", photoFile)
//                pictureIV!!.setImageURI(uri)
//
//                val storage = FirebaseStorage.getInstance()
//                val storageRef = storage.reference
////                val imageRef = storageRef.child("images/${photoFile.name}")
//                val email = FirebaseAuth.getInstance().currentUser?.email
//                val userId = FirebaseAuth.getInstance().currentUser?.uid
//                val imageRef = storageRef.child("images/$userId/${photoFile.name}")
//                val uploadTask = imageRef.putFile(uri)
//
////                val email = FirebaseAuth.getInstance().currentUser?.email
//                val usersRef = FirebaseUtils.databaseInstance.getReference("users")
//
//                usersRef.orderByChild("email").equalTo(email).addListenerForSingleValueEvent(object : ValueEventListener {
//                    override fun onDataChange(snapshot: DataSnapshot) {
//                        if (snapshot.exists()) {
//                            uploadTask.addOnSuccessListener {
//
//                                // L'utilisateur a été trouvé dans la base de données Firebase
//                                val userId = snapshot.children.first().key.toString()
//                                val photosRef =
//                                    FirebaseUtils.databaseInstance.getReference("users/$userId/photos")
//                                Log.d("User ID", userId)
//
//                                // Ici vous pouvez ajouter le code pour enregistrer la photo dans la base de données Firebase
//
////                                val photoId = photosRef.push().key
////                                Log.d("Photo Id", photoId.toString())
//
////                                val photoUrl = imageRef.toString()
////                                Log.d("Photo URL", photoUrl)
//                                // Utilise l'URL HTTPS
//                                val storageRef = imageRef
//                                storageRef.downloadUrl.addOnSuccessListener { uri ->
//                                    val photoId = photosRef.push().key
//                                    Log.d("Photo Id", photoId.toString())
//
//                                    val photoUrl = uri.toString()
//                                    Log.d("Photo URL", photoUrl)
//
//                                    Log.d("Image url", imageRef.toString())
//
//                                    val photo = Photo(photoId!!, photoUrl, HashMap())
//                                    photosRef.child(photoId ?: "").setValue(photo)
//
//                                    /*recharger la liste des photos*/
//                                    Log.d("image url", photoUrl)
////                                    Log.d("Before Add photo", photos.toString())
////
////                                    photos.add(photo)
////                                    Log.d("After Add photo", photos.toString())
//
////                                    val adapter = ImageAdapter(requireContext(), photos)
////                                    recyclerView.adapter = adapter
//
//                                    val filename = photoUrl.substringAfterLast("/")
//                                    Log.d("Image Name", filename)
//
//                                    val storageRef = Firebase.storage.reference.child("images/$userId/$filename")
//
//                                    // Télécharger l'image dans Firebase Storage
//                                    storageRef.putFile(uri).addOnSuccessListener { taskSnapshot ->
//                                        // Récupérer le lien de l'image dans Firebase Storage
////                                        val photoUrl = taskSnapshot.metadata?.reference?.downloadUrl.toString()
//
//                                        // Ajouter la photo à la liste des photos
//                                        Log.d("Before Add photo", photos.toString())
//
//                                        photos.add(photo)
//                                        Log.d("After Add photo", photos.toString())
//
//                                        // Mettre à jour l'adaptateur de RecyclerView
//                                        val adapter = ImageAdapter(requireContext(), photos)
//
//                                        adapter.notifyDataSetChanged()
//                                        recyclerView.adapter = adapter
//                                    }.addOnFailureListener { e ->
//                                        // Gérer les erreurs de téléchargement de l'image
//                                        Log.e(TAG, "Error uploading image to Firebase Storage: $e")
//                                    }
//                                    /**/
//
//                                    /*recharger la liste des photos*/
////                                    initRecyclerView()
//
//                                }.addOnFailureListener { exception ->
//                                    // Gérer l'erreur
//                                }
//                            }.addOnFailureListener { exception ->
//                                if (FirebaseAuth.getInstance().currentUser != null) {
//                                    Log.d("Utilisateur connecté", FirebaseAuth.getInstance().currentUser.toString())
//                                } else {
//                                    Log.d("Utilisateur non connecté", "Aucun utilisateur connecté")
//                                }
//                                Log.d("error image", exception.message.toString())
//                                Toast.makeText(context, "Erreur lors du téléchargement de la photo: ${exception.message}", Toast.LENGTH_SHORT).show()
//                            }
//                        } else {
//                            // L'utilisateur n'a pas été trouvé dans la base de données Firebase
//                            Toast.makeText(context, "Utilisateur introuvable", Toast.LENGTH_SHORT).show()
//                        }
//                    }
//
//                    override fun onCancelled(error: DatabaseError) {
//                        // Une erreur s'est produite lors de la recherche de l'utilisateur dans la base de données Firebase
//                        Toast.makeText(context, "Erreur : ${error.message}", Toast.LENGTH_SHORT).show()
//                    }
//                })
//
//            }
//            else {
//                super.onActivityResult(requestCode, resultCode, data)
//            }
//        } catch (e: Exception) {
//            Toast.makeText(requireContext(), "Erreur: ${e.message}", Toast.LENGTH_SHORT).show()
//        }
//    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
