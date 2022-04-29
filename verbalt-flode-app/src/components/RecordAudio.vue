<template>
  <div class="record">
    <button v-if="recording" @click="stop()">Stop Recording</button>
    <button v-else @click="start()">Start Recording</button>

    <button v-if="mp3.url != mp3Comp.url" @click="play()">Playback</button>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import microm from "../main";
import { createPresignedPost } from "@aws-sdk/s3-presigned-post";
import { S3Client } from "@aws-sdk/client-s3";
import { createReadStream } from "node_modules/fs";
import FormData from "form-data";

export default Vue.extend({
  name: "message",
  props: {},
  data() {
    return {
      recording: false,
      mp3: {
        url: "hhh",
        blob: "flkdnf",
        buffer: "dsfjhlkjf"
      },
      mp3Comp: {
        url: "hhh",
        blob: "flkdnf",
        buffer: "dsfjhlkjf"
      },
      stream: {
        getAudioTracks: function() {
          return [{stop}]
        }
      }
    };
  },
  methods: {
    start: async function() {

      this.recording = true;
      let s = await microm.record()
      this.stream = s;
      console.log("recording...");
    },
    play: function() {
      microm.play();
    },
    download: function() {
      var fileName = "cat_voice";
      microm.download(fileName);
    },
    stop: async function() {
      this.recording = false;
      let result = await microm.stop()
      this.mp3 = result;
      console.log(this.mp3.url, this.mp3.blob, this.mp3.buffer);
      var newMP3 = microm.getMp3();
      console.log(newMP3);
      this.download();
      this.stream.getAudioTracks().forEach(track => track.stop());
    },
    post: function() {
      const d = new Date();
      let time = d.getTime();

      const client = new S3Client({ region: "us-west-2" });
      const Bucket = "johnsmith";
      const Key = "user/eric/1";
      const Fields = {
        acl: "public-read",
      };

      

      const form = new FormData();
      Object.entries(Fields).forEach(([field, value]) => {
        form.append(field, value);
      });
      form.append("file", createReadStream("path/to/a/file"));
      form.submit("https://2ug9xdpzd2.execute-api.us-east-1.amazonaws.com/tests/", (err, res) => {
        //handle the response
      });
    }
  },
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
