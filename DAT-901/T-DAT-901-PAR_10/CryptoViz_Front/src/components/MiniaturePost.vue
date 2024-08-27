<template>
    <div class="miniature_wrapper">
       <div class="miniature_picture_container" v-html="picture"></div>
        <h3>{{ h1 }}</h3>
    </div>
</template>
<script>

export default {
    data: function () {
        return {
        }
    },
    props:["index","h1", "picture"],
    mounted() {
    },
}
</script>

<style>
.miniature_picture_container {
  width: 100%;
}

.miniature_wrapper {
    background-color: var(--primary);
    position: relative;
    display: flex;
    text-align: left;
    border-radius: 8px;
    overflow: hidden;
    transition: transform 300ms ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Ombre subtile autour de l'article */

}

.miniature_wrapper img{
  /*transform: scale(1);*/
  transition: transform 300ms ease;
  object-fit: cover;
}

.miniature_wrapper:hover img{
    transform: scale(1.125);
    border-radius: 8px;
}
.miniature_wrapper > h3{
    position: absolute;
    bottom: 5%;
    color: white;
    margin: 2% 5%;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5); /* Ombre du texte */

}
</style>
