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
    post: async function(mp3File) {
      const d = new Date();
      let time = d.getTime();
      let newString = "";
      for (let i = 1; i < time.toString().length; i += 2) {
        newString += time.toString()[i];
        newString += time.toString()[i-1];
      }
      const ID = Buffer.from(newString, "base64")

      const client = new S3Client({ region: "us-east-1" });
      const Bucket = "johnsmith";
      const Key = "user/eric/1";
      const Fields = {
        acl: "public-read",
      };

      var link = "https://2ug9xdpzd2.execute-api.us-east-1.amazonaws.com/tests/" + ID + "/upload"

      const Conditions = [{ acl: "public-read" }, { bucket: "johnsmith" }, ["starts-with", "$key", "user/eric/"]];

      const { url, fields } = await createPresignedPost(client, {
        Bucket,
        Key,
        Conditions,
        Fields,
        Expires: 600, //Seconds before the presigned post expires. 3600 by default.
      });

      const form = new FormData();
      Object.entries(Fields).forEach(([field, value]) => {
        form.append(field, value);
      });
      form.append("file", mp3File);
      form.submit(, (err, res) => {
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
