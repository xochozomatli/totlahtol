import styled from 'styled-components'

const Hint = styled.form`
  position: absolute;
  top: 1.8rem;
`

const Word = styled.span`
  cursor: pointer;
`
const Punct = styled.span`
`

const Body = styled.div`
  position: relative;
  display: inline-block;
  margin: .2rem .1rem;
  padding: .2rem .1rem 1rem .1rem;
  & > ${Hint} {
    display: ${ props => props.showHint===true ? "block" : "none"};
    & > input{border: solid ${ props => props.seen===true ? "#ba421e" : "#5fa348"}};
  };
  & > ${Word} {
    border-bottom: solid ${ props => props.seen===true ? "#ba421e" : "#5fa348"};
  }
  & > ${Punct} {
    border-bottom: none;
    white-space: pre;
  }
`

export {Hint, Word, Punct, Body}
