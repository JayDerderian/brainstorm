import React from "react";
import "../App.css";
import "./AboutUs.css";
import { Link } from "react-router-dom";

function AboutUs() {
  return (
    <div className="about-container">
      <div className="top">
        <h1 className="about">.about</h1>
        <p className="appDez">
          BrainStorm is a web application to help users in the creative process
          by <br></br>providing pseudo-randomly generated melodic ideas. This is
          achieved by utilizing <br></br>Python's built-in random() module in
          conjunction with a variety of mapping techniques <br></br> to make
          "decisions" about how to generate melodies based off several <br></br>
          different kinds of inputs. For this project, we used Python for the
          back-end and <br></br>
          CSS, Javascript, React for the front-end. We hope you enjoy your
          melody!
        </p>
        <h2 className="webDev">Web Developers:</h2>
      </div>
      <div className="bottom">
        <h3 className="jayName">Jay Derderian</h3>
        <div className="about-wrapper">
          <img
            className="jayFake"
            src="/images/einstein.jpeg"
            alt="synth cat in space"
          ></img>
          <img
            className="jayPic"
            src="/images/jayBW.jpg"
            alt="just another cat"
          ></img>
        </div>
        <p className="jayDez">Backend composer and fearless leader</p>
        <h3 className="jaredName">Jared Goldsmith</h3>
        <div className="about-wrapper">
          <img
            className="jaredFake"
            src="/images/einstein.jpeg"
            alt="synth cat in space"
          ></img>
          <img
            className="jaredPic"
            src="/images/jared2.jpg"
            alt="just another cat"
          ></img>
        </div>
        <p className="jaredDez">Frontend Reactionary and CSS laborer</p>
        <h3 className="ericName">Eric Dale</h3>
        <div className="about-wrapper">
          <img
            className="ericFake"
            src="/images/einstein.jpeg"
            alt="a baboon trapeze artist"
          ></img>
          <img
            className="ericPic"
            src="/images/eric.jpg"
            alt="thirty gorillas in a trenchcoat"
          ></img>
        </div>
        <p className="ericDez">
          The monkey putting together the Legos, <br></br>connecting both the frontend
          and the backend
        </p>
        <h4 className="github">
          <a href="https://github.com/not-eric/brainstorm" className="gitlink">
            Github
          </a>
        </h4>
      </div>
      <div className="bottombottom">
        <p className="copyRight">&copy; BrainStorm</p>
      </div>
    </div>
  );
}

export default AboutUs;
