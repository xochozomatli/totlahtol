import styled from 'styled-components'

const Background = styled.div`
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
  transform: scale(1.1)
`

const Body = styled.div`
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  height: 75vh;
  width: 36rem;
  border-radius: 0.5rem;
`
const Header = styled.header`
  display: flex;
  justify-content: space-between;
  box-sizing: border-box;
  width: 100%;
  margin: 0 auto;
  background: #f5f6f7;
  padding: .5rem 1rem;
  border: 1px solid #dddfe2;
  border-radius: 5px 5px 0px 0px;
  border-bottom: 0px;
`

const Title = styled.span`
  font-size: 1.5rem;
  font-weight: 700;
  color: #444;
`

const Button = styled.button`
  margin: .5rem;
 `

const Content = styled.div`
  display: ${ props => props.user===true ? "block" : "flex"};
  flex-wrap: wrap;
  box-sizing: border-box;
  width: 100%;
  padding: .5rem 1rem;
`

const Exit = styled.div`
  position: absolute;
  left: -5%;
  top: .75rem;
  height: 1.5rem;
  width: 1.5rem;
  cursor: pointer;
`
const TextBox = styled.textarea`
  padding: 1rem;
  ${'' /* border: none; */}
  margin-bottom: 1rem;
  font-size: 1rem;
  height: 60vh;
  width: 100%;
  border-radius: 5px;
  resize: none;
  outline: none;
`;

const Field = styled.div`
  margin: 1.5rem .5rem;
  & > span {
    color: #555;
  }
  & > input {
    display: block;
    width: 320px;
    border: none;
    border-bottom: 1px solid #dddfe2;
    font-size: 1.25rem;
    outline: none
  }
`
const Success = styled.div`
  background-color: green;
`;

const Error = styled.div`
  background-color: red;
`;

export {Background, Body, Header, Title, Button, Content, Exit, TextBox, Field, Success, Error}