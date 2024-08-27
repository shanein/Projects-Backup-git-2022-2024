package com.example.myapplication

import android.os.Bundle
import android.text.TextUtils
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.example.myapplication.databinding.FragmentRegisterBinding
import com.google.firebase.auth.FirebaseAuth
import java.util.regex.Pattern
import android.util.Log


class RegisterFragment : Fragment() {

    private var _binding: FragmentRegisterBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        _binding = FragmentRegisterBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Vérifier si l'utilisateur est déjà connecté
        val currentUser = FirebaseAuth.getInstance().currentUser
        if (currentUser != null) {
            findNavController().navigate(R.id.action_RegisterFragment_to_SecondFragment)
            return
        }

        binding.buttonCreateAccount.setOnClickListener {
            val firstName = binding.editTextFirstName.text.toString()
            val lastName = binding.editTextLastName.text.toString()
            val email = binding.editTextEmail.text.toString()
            val password = binding.editTextPassword.text.toString()

            if (TextUtils.isEmpty(firstName)) {
                binding.editTextFirstName.error = "First name is required"
                return@setOnClickListener
            }

            if (TextUtils.isEmpty(lastName)) {
                binding.editTextLastName.error = "Last name is required"
                return@setOnClickListener
            }

            if (TextUtils.isEmpty(email)) {
                binding.editTextEmail.error = "Email is required"
                return@setOnClickListener
            }

            if (TextUtils.isEmpty(password)) {
                binding.editTextPassword.error = "Password is required"
                return@setOnClickListener
            }

            //Sécurité pour le password
            val passwordPattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$"
            val pattern = Pattern.compile(passwordPattern)
            val matcher = pattern.matcher(password)

            if (!matcher.matches()) {
                binding.editTextPassword.error = "The password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character"
                return@setOnClickListener
            }

            FirebaseAuth.getInstance().createUserWithEmailAndPassword(email, password)
                .addOnCompleteListener { task ->
                    if (task.isSuccessful) {
                        val userId = FirebaseAuth.getInstance().currentUser?.uid
                        val databaseReference = FirebaseUtils.databaseInstance.getReference("users")

                        val user = HashMap<String, Any>()
                        user["firstName"] = firstName
                        user["lastName"] = lastName
                        user["email"] = email

                        databaseReference.push().setValue(user).addOnCompleteListener {
                            Log.d("RealtimeDatabase", "test") // Ajout d'un message de confirmation

                            if (it.isSuccessful) {
                                Log.d("RealtimeDatabase", "User data added to Realtime Database") // Ajout d'un message de confirmation
                                findNavController().navigate(R.id.action_RegisterFragment_to_SecondFragment)
                            } else {
                                Log.e("RealtimeDatabase", "Error adding user data to Realtime Database: ${it.exception?.message}") // Ajout d'un message d'erreur
                                Toast.makeText(context, "Error: ${it.exception?.message}", Toast.LENGTH_SHORT).show()
                            }
                        }.addOnFailureListener { exception ->
                            Log.e("RegisterFragment", "Erreur lors de l'ajout de l'utilisateur à la base de données", exception)
                            Toast.makeText(context, "Erreur lors de l'ajout de l'utilisateur à la base de données", Toast.LENGTH_SHORT).show()
                        }
                    } else {
                        Toast.makeText(context, "Error: ${task.exception?.message}", Toast.LENGTH_SHORT).show()
                    }
                }
        }

        binding.buttonSigninRegister.setOnClickListener {
            findNavController().navigate(R.id.action_RegisterFragment_to_FirstFragment)
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
