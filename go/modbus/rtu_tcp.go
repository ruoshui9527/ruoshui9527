package main

import (
	"encoding/json"
	"fmt"
	"github.com/rs/cors"
	"github.com/simonvetter/modbus"
	"io/ioutil"
	"log"
	"net/http"
	"time"
)

// 定义一个结构体来表示请求体
type RequestBody struct {
	DeviceIp string `json:"deviceIp"` // 假设我们要获取的键是 "key"
}

// 定义一个结构体来表示响应体
type ResponseBody struct {
	Msg  string `json:"msg"`
	Code int16  `json:"code"`
	Data int16  `json:"data"`
}

func mes_modbus(w http.ResponseWriter, r *http.Request) {
	// 读取请求体
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Failed to read request body", http.StatusBadRequest)
		return
	}
	defer r.Body.Close()

	// 解析 JSON 请求体
	var requestBody RequestBody
	if err := json.Unmarshal(body, &requestBody); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	// 获取特定键的内容
	keyValue := requestBody.DeviceIp
	fmt.Printf(keyValue)

	var client *modbus.ModbusClient

	// for an RTU over TCP device/bus (remote serial port or
	// simple TCP-to-serial bridge)
	client, err = modbus.NewClient(&modbus.ClientConfiguration{
		URL:     fmt.Sprintf("rtuovertcp://%s:8899", keyValue),
		Speed:   19200, // serial link speed
		Timeout: 1 * time.Second,
	})

	if err != nil {
		// error out if client creation failed
		fmt.Printf("error1: %s", err)
	}

	// now that the client is created and configured, attempt to connect
	err = client.Open()
	if err != nil {
		fmt.Printf("error2: %s", err)
	}

	defer func() {
		if r := recover(); r != nil {
			log.Printf("捕获到 panic: %v", r)
			writeResponse(w, 200, "fail", 0)
		}
	}()

	var reg16s []uint16
	reg16s, err = client.ReadRegisters(33, 2, modbus.HOLDING_REGISTER)

	writeResponse(w, 200, "success", int16(reg16s[1]))

	// close the TCP connection/serial port
	client.Close()
}

func writeResponse(w http.ResponseWriter, code int16, msg string, data int16) {
	response := ResponseBody{
		Msg:  msg,
		Code: code,
		Data: data,
	}

	// 设置响应头为 JSON
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	// 返回 JSON 响应
	json.NewEncoder(w).Encode(response)
}

func main() {
	corsOpts := cors.New(cors.Options{
		AllowedOrigins:   []string{"*"}, 
		AllowedMethods:   []string{"GET", "POST", "PUT", "DELETE"},
		AllowedHeaders:   []string{"*"},
		AllowCredentials: true, // 是否允许发送 cookie
	})

	// 将 CORS 中间件应用到你的 HTTP 处理函数
	http.Handle("/deviceInfo", corsOpts.Handler(http.HandlerFunc(mes_modbus)))
	http.ListenAndServe(":1423", nil) // 启动服务器
}
