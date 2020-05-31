import styled from 'styled-components';

const Header = styled.header`
  height: 42px;
  background-color: #5fa348;
  margin-bottom: 1rem;
`

const CardTitle = styled.div`
  box-sizing: border-box;
  max-width: 510px;
  margin: 0 auto;
  background: #f5f6f7;
  font-size: 1rem;
  font-weight: 700;
  color: #444;
  padding: .5rem;
  border: 1px solid #dddfe2;
  border-radius: 5px 5px 0px 0px;
  border-bottom: 0px;
`

const Card = styled.div`
  box-sizing: border-box;
  max-width: 510px;
  margin: 0 auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #fff;
  border: 1px solid #dddfe2;
  border-radius: 0px 0px 5px 5px;
`;

const Form = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
`;

const Input = styled.input`
  padding: 1rem;
  border: none;
  font-size: .8rem;
  border-bottom: 1px solid #dddfe2;
  outline: none;
`;

const TextBox = styled.textarea`
  padding: 1rem;
  border: none;
  margin-bottom: 1rem;
  font-size: 1rem;
  height: 20vh;
  border-radius: 5px;
  resize: none;
  outline: none;
`;

const Button = styled.button`
  background: #ba421e;
  border: 1px solid #ba421e;
  border-radius: 2px;
  padding: .5rem;
  color: white;
  font-weight: 700;
  width: 100%;
  margin-bottom: 0rem;
  font-size: 0.8rem;
`;

const Logo = styled.img`
  width: 50%;
  margin-bottom: 1rem;
`;

const Error = styled.div`
  background-color: red;
`;

export { Header, Form, Input, TextBox, Button, Logo, Card, CardTitle, Error };