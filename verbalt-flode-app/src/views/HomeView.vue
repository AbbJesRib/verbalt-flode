<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <record-audio></record-audio>
  </div>
</template>

<script>
// @ is an alias to /src
import RecordAudio from '@/components/RecordAudio.vue';

export default {
  name: 'HomeView',
  components: {
    RecordAudio
  }
}
</script>
