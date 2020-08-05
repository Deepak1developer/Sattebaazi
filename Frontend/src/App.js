import React from 'react'
import { Layout, Table, Row, Col,Spin } from 'antd'
import axios from 'axios';
import { constants, columns } from './constants'
import Search from '../src/util/search/search'
// Styles.
import './App.css'
class App extends React.Component {

  state = {
    ready: false,
    word :''
  };
  async componentWillMount () {await axios.get(`https://47314105.ngrok.io/nifty_50`)
  .then(res => {
    const word = res.data;
    this.setState({ word,ready: true });
  })
  }

  getMarketDataRender () {
    return <div>
      {this.state.ready &&
      <div>
        <Row justify='left' type='flex'>
          <Col span={10}><h3>Stocks Stats</h3></Col>
          <Col span={10}>
            <Search/>
          </Col>
        </Row>
        <br />
        <Table
          size='small'
          style={{ minWidth: '1000px' }}
          pagination={false}
          rowKey={record => record.category}
          columns={columns.MarketData}
          dataSource={this.state.word}
        />
      </div>
      }
    </div>
  }
  render () {
    return (
      <Layout className='layout'>
        <Layout.Header style={{textAlign:"center"}}>
          <h1 style={{ color:"rgb(255,255,255)"}}>😃 Market Guru 😃</h1>
        </Layout.Header>
        <Layout.Content style={{ padding: '5vh 5vw 0vh 5vw', backgroundColor: '#FFF', minHeight: '70vh' }}>
          {this.state.ready
            ? <div>
              {this.getMarketDataRender()}
              <br />
            </div>
            : <center>
              <h1>Loading...</h1>
              <Spin size='large' />
            </center>
          }
        </Layout.Content>
        <Layout.Footer>
          <center>UI creator team TheBigShot</center>
        </Layout.Footer>
      </Layout>
    )
  }
}

export default App
