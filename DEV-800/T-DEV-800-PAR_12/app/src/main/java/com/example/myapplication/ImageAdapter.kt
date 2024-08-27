package com.example.myapplication

import android.content.Context
import android.content.Intent
import android.graphics.drawable.Drawable as AndroidDrawable
import com.bumptech.glide.load.resource.drawable.DrawableResource as GlideDrawableResource
import android.net.Uri
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.bumptech.glide.load.DataSource
import com.bumptech.glide.load.engine.GlideException
import com.bumptech.glide.request.RequestListener
import com.google.gson.Gson


class ImageAdapter(private val context: Context, private val images: ArrayList<ListFragment.Photo>, private val userPhotoId: String? = null) : RecyclerView.Adapter<ImageAdapter.ViewHolder>() {

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val imageView: ImageView = view.findViewById(R.id.image_view) // ImageView pour afficher l'image
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.image_item, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
//        // Convertir le lien en un objet Uri
        val uri = Uri.parse(images[position].url)
        Log.d("ImageAdapter", "Image URL: ${images[position].url}")
        Log.d("ImageAdapter", "Image ID: ${images[position].id}")
//
//        // Charger l'image dans ImageView à partir de l'URL distante en utilisant setImageURI
//        holder.imageView.setImageURI(uri)

        val listener = object : RequestListener<AndroidDrawable> {
            override fun onLoadFailed(e: GlideException?, model: Any?, target: com.bumptech.glide.request.target.Target<AndroidDrawable>?, isFirstResource: Boolean): Boolean {
                Log.e("ImageAdapter", "Error loading image: $e")
                return false
            }
            override fun onResourceReady(resource: AndroidDrawable?, model: Any?, target: com.bumptech.glide.request.target.Target<AndroidDrawable>?, dataSource: DataSource?, isFirstResource: Boolean): Boolean {
                return false
            }
        }

        holder.imageView.setImageURI(uri)

        Glide.with(context)
            .load(uri)
            .listener(listener)
            .into(holder.imageView)

//         Set an OnClickListener on the ImageView to launch the ImageDetailActivity
        holder.imageView.setOnClickListener {
            val intent = Intent(context, ImageDetailActivity ::class.java)
            Log.e("ImageAdapter click", images[position].url)

            val photoJson = Gson().toJson(images[position])
            intent.putExtra(ImageDetailActivity.EXTRA_IMAGE_URL, photoJson)
            if (userPhotoId != null) {
                intent.putExtra(ImageDetailActivity.EXTRA_IMAGE_USER_ID, userPhotoId)
            }


            context.startActivity(intent)
        }
    }

    override fun getItemCount(): Int {
        return images.size
    }
}
