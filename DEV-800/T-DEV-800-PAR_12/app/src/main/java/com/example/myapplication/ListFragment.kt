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
import com.example.myapplication.databinding.FragmentListBinding
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


class ListFragment : Fragment() {

    private lateinit var recyclerView: RecyclerView // RecyclerView pour afficher les images

    private var _binding: FragmentListBinding? = null
    private val binding get() = _binding!!

    private var pictureIV  : ImageView? = null
    private lateinit var photoFile: File
    private lateinit var currentPhotoPath: String
    private val PICTURE_FROM_CAMERA: Int = 1

//    private val urls = ArrayList<String>()
    private val photos = ArrayList<Photo>()
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        _binding = FragmentListBinding.inflate(inflater, container, false)

        initView()


        recyclerView = binding.recyclerView
        recyclerView.layoutManager = GridLayoutManager(requireContext(), 3) // Afficher les images en grille 3x3

        initRecyclerView()

        val sharedPicturesButton = binding.sharedPictures
        sharedPicturesButton.setOnClickListener {
            // Code pour rediriger vers la page "sharedpictures"
            // Utilisez ici l'intent ou la méthode de navigation appropriée en fonction de votre architecture d'application
            findNavController().navigate(R.id.action_ListFragment_to_ListFragmentShared)
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
                    val userId = snapshot.children.first().key.toString()
                    val photosRef = FirebaseUtils.databaseInstance.getReference("users/$userId/photos")
                    photosRef.addListenerForSingleValueEvent(object : ValueEventListener {
                        override fun onDataChange(snapshot: DataSnapshot) {
//                            val urls = ArrayList<String>()
                            for (photoSnapshot in snapshot.children) {
                                val photoId = photoSnapshot.key // Récupère l'identifiant de la photo
                                val photo = photoSnapshot.getValue(Photo::class.java)
                                photo?.let {
                                    val url = it.url
                                    val photoObject = Photo(photoId!!, url) // Crée un nouvel objet Photo avec l'ID et l'URL de la photo
                                    photos.add(photoObject) // Ajoute l'objet Photo à la liste
                                }
                            }
                            Log.d("urls photos", photos.toString())
                            // Utilisez la liste des URLs pour afficher les photos dans votre RecyclerView
                            val adapter = ImageAdapter(requireContext(), photos) // Adapter pour gérer l'affichage des images
                            recyclerView.adapter = adapter
                        }

                        override fun onCancelled(error: DatabaseError) {
                            // Une erreur s'est produite lors de la récupération des photos depuis Firebase
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

    data class Photo(
        val id: String = "",
        val url: String = "",
        val sharedWith: HashMap<String, Boolean> = HashMap()
    )

    private fun initView() {
        pictureIV = binding.picture
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)


        binding.buttonTakePhoto.setOnClickListener {
            if (ContextCompat.checkSelfPermission(requireContext(), Manifest.permission.CAMERA)
                != PackageManager.PERMISSION_GRANTED
            ) {
                ActivityCompat.requestPermissions(
                    requireActivity(),
                    arrayOf(Manifest.permission.CAMERA),
                    PICTURE_FROM_CAMERA
                )
            } else {
                takePicture()
            }
        }
    }

    private fun takePicture() {
        try {
            val pictureIntent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
            photoFile = createImageFile()
            Log.d("Chemin du fichier", photoFile.absolutePath)
            val uri = FileProvider.getUriForFile(
                requireContext(),
                "com.example.myapplication.fileprovider",
                photoFile
            )
            pictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, uri)
            startActivityForResult(pictureIntent, PICTURE_FROM_CAMERA)
        } catch (e: Exception) {
            e.printStackTrace()
            Toast.makeText(requireContext(), "Erreur lors de la prise de photo : ${e.message}", Toast.LENGTH_SHORT).show()
        }
    }

    private fun createImageFile(): File {
        val timeStamp: String = SimpleDateFormat("yyyyMMdd_HHmmss").format(Date())
        val storageDir: File? = requireContext().getExternalFilesDir(
            Environment.DIRECTORY_PICTURES
        )
        return File.createTempFile("JPEG_${timeStamp}_", ".jpg", storageDir).apply {
            currentPhotoPath = absolutePath
        }
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
                                val photo = Photo(photoId!!, photoUrl, HashMap())
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

    //function pour supprimer une photo dans la liste
    fun deletePhoto(photo: Photo) {
        photos.remove(photo)
        recyclerView.adapter?.notifyDataSetChanged()
    }

    //Gestion de permission camera sur le tel
    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        when (requestCode) {
            PICTURE_FROM_CAMERA -> {
                if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    takePicture()
                }
                return
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
