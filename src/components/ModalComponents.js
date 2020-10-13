import styled from 'styled-components'

const ModalBackground = styled.div`
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
  transform: scale(1.1)
`

const ModalBody = styled.div`
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  height: 75vh;
  width: 36rem;
  border-radius: 0.5rem;
`

const ModalTitle = styled.div`
  box-sizing: border-box;
  width: 100%;
  margin: 0 auto;
  background: #f5f6f7;
  font-size: 1.5rem;
  font-weight: 700;
  color: #444;
  padding: .5rem 1rem;
  border: 1px solid #dddfe2;
  border-radius: 5px 5px 0px 0px;
  border-bottom: 0px;
`

const ModalContent = styled.div`
  display: flex;
  flex-wrap: wrap;
  box-sizing: border-box;
  width: 100%;
  padding: .5rem 1rem;
`

const ModalExit = styled.div`
  position: absolute;
  left: -5%;
  top: .75rem;
  height: 1.5rem;
  width: 1.5rem;
  cursor: pointer;
`

const TlahtolliHint = styled.form`
  visibility: hidden;
  width: 180px;
  background-color: black;
  color: #fff;
  text-align: center;
  padding: 5px 0;
  border-radius: 6px;
  bottom: 100%;
  left: 50%;
  margin-left: -60px;

  position: absolute;
  z-index: 1;
  
`

const Tlahtolli = styled.div`
  position: relative;
  display: inline-block;
  margin: .8rem .2rem;
  padding: .1rem;
  border-bottom: solid ${ props => props.seen==true ? "#ba421e" : "#5fa348"};
  cursor: pointer;
  ${'' /* &:hover ${TlahtolliHint} {
    visibility: visible; */}
  }
`

export {ModalBackground, ModalBody, ModalTitle, ModalContent, ModalExit, Tlahtolli, TlahtolliHint}