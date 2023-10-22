import { useEffect, useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import React, { useRef } from "react";
import "./App.css";

import firebase from "firebase/compat/app";
import "firebase/compat/firestore";
import "firebase/compat/auth";
import "firebase/compat/analytics";
import { useAuthState } from "react-firebase-hooks/auth";
import { useCollectionData } from "react-firebase-hooks/firestore";
import rawTxt from "D:/Saumya/Development/c-bytes/CS-GH-analysis/ghFile/softmove.txt";

// import styles from "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
} from "@chatscope/chat-ui-kit-react";
import image from "./1.png";
firebase.initializeApp({
  apiKey: "AIzaSyDkzeUxy0N3uRUY1bqrNW-mFNSWYelzu3s",
  authDomain: "c-byte.firebaseapp.com",
  projectId: "c-byte",
  storageBucket: "c-byte.appspot.com",
  messagingSenderId: "95089779254",
  appId: "1:95089779254:web:e9aa371ac18f2381826e97",
  measurementId: "G-3LX31R2PYX",
});

import data from "./output.json"; // Replace with your JSON URL
console.log(data[0]);
const gh_files = data.map((topic) => {
  return topic.topics.id;
});
console.log(gh_files);
const auth = firebase.auth();
const firestore = firebase.firestore();
const analytics = firebase.analytics();

function App() {
  const [user] = useAuthState(auth);

  return (
    <div className="App">
      <header>
        <h1></h1>
        <SignOut />
      </header>

      <section>{user ? <ChatRoom /> : <SignIn />}</section>
    </div>
    // </div>
  );
}

function SignIn() {
  const signInWithGoogle = () => {
    const provider = new firebase.auth.GoogleAuthProvider();
    auth.signInWithPopup(provider);
  };

  return (
    <>
      <button className="sign-in" onClick={signInWithGoogle}>
        Sign in with Google
      </button>
    </>
  );
}

function SignOut() {
  return (
    auth.currentUser && (
      <button className="sign-out" onClick={() => auth.signOut()}>
        Sign Out
      </button>
    )
  );
}

function ChatRoom() {
  const dummy = useRef();
  const messagesRef = firestore.collection("messages");
  const query = messagesRef.orderBy("createdAt").limit(25);

  const [messages] = useCollectionData(query, { idField: "id" });

  const [formValue, setFormValue] = useState("");
  const [fileContent, setFileContent] = useState("");

  useEffect(() => {
    const handleFileChange = () => {
      fetch(rawTxt)
        .then((r) => r.text())
        .then((text) => {
          setFileContent(text);
        });
    };
    handleFileChange();
  });
  const sendMessage = async (e) => {
    e.preventDefault();

    const { uid, photoURL } = auth.currentUser;
    console.log(formValue);
    await messagesRef.add({
      text: formValue,
      createdAt: firebase.firestore.FieldValue.serverTimestamp(),
      uid,
      photoURL,

      // displayName: "string | null",
      // email: "string | null",
      // phoneNumber: "string | null",
      // providerId: "string",
      // uid: "string",
    });
    if (formValue.includes("hello")) {
    } else if (formValue.includes(".gh")) {
      await messagesRef.add({
        text:
          "Here is some information about the grasshoper file " + fileContent,
        createdAt: firebase.firestore.FieldValue.serverTimestamp(),
        uid: "x0gS8dSQScO1AZg3XHEt",
      });
    } else if (formValue.includes("tell")) {
      // Create a JSON object with the input text
      const data = {
        input_text: formValue,
      };

      // Define the URL of your Flask API
      const apiUrl = "http://localhost:5000/compute_similarity";

      // Send a POST request to the API using the fetch API
      fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => response.json())
        .then((data) => {
          // Handle the response from the API
          console.log("Cosine similarity:", data.cosine_similarity);
        })
        .catch((error) => {
          // Handle any errors
          console.error("Error:", error);
        });

      await messagesRef.add({
        // text: "According to the discussions, there is a way to use the softmove tool using grasshoper. You can use this softmove.gh to test things out",
        text: "According to the discussions, I found this to be helpful ", //+
        createdAt: firebase.firestore.FieldValue.serverTimestamp(),
        uid: "x0gS8dSQScO1AZg3XHEt",
      });
    }

    setFormValue("");
    dummy.current.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <>
      <main>
        {messages &&
          messages.map((msg) => <ChatMessage key={msg.id} message={msg} />)}

        <span ref={dummy}></span>
      </main>

      <form onSubmit={sendMessage}>
        <input
          value={formValue}
          onChange={(e) => setFormValue(e.target.value)}
          placeholder="Ask questions regarding Grasshoper"
        />

        <button type="submit" disabled={!formValue}>
          🕊️
        </button>
      </form>
    </>
  );
}

function ChatMessage(props) {
  const { text, uid, photoURL } = props.message;

  const messageClass = uid === auth.currentUser.uid ? "sent" : "received";

  return (
    <>
      <div className={`message ${messageClass}`}>
        <img src={photoURL || image} />
        <p>{text}</p>
      </div>
    </>
  );
}

export default App;
