// import React from "react";

// const Ranking = () => {
//   return (
//     <>
//       <p className="ranking">Ranking goes here...</p>
//     </>
//   );
// };

// export default Ranking;

import React, { useState, useEffect } from 'react';

const ParsedData = () => {
  const [parsedData, setParsedData] = useState([]);
  // const [extracted,setExtracted] = useState([])

  useEffect(() => {
    // Fetch parsed data from backend when component mounts
    fetchData();
  }, []);

  const fetchData = async () => {
    const myHeaders = new Headers();
    // myHeaders.append("Cookie", "csrftoken=UQvwyv09vPRqC5RBEP4QqT6hAg9oWQol");

    const requestOptions = {
      method: "GET",
      headers: myHeaders,
      redirect: "follow"
    };

    fetch("http://127.0.0.1:8000/get_parsed_data/", requestOptions)
      .then((response) => response.text())
      .then((result) => {
        // console.log(result)
        const value = JSON.parse(result)
        setParsedData(value.parsed_data)
        
        // const v = JSON.parse(parsedData.extracted_data)
        // console.log(v)
        // console.log(value.parsed_data)
      })
      .catch((error) => console.error(error));
  };
   console.log(parsedData)


  
  return (
    <div>
      <h1>Parsed Data</h1>
      <ul>
        {parsedData.map((item) => (

          <li key={item.id}>

            <h3>ID: {item.id}</h3>
            <p>Extracted Data: {item.name}</p>
            <p>Extracted Data: {item.skills}</p>
            <p>Extracted Data: {item.experience}</p>
            <p>Extracted Data: {item.certifiacation}</p>
            

          </li>
        ))}
      </ul>
    </div>
  );

        }   
export default ParsedData;
