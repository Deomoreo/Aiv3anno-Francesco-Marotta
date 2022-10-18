.org $8000
start:
    LDX #$FF
    TXS

    LDX #0
    LDA #1
    JSR RandomStartColor ;Random color when reset, if reset cell 00 dont work
    
    LDX #0
    LDA #1
    JSR ClearZeroPage
    

    LDX #00  ; start x 
    STX $00
    LDX #00  ; start y 
    STX $01
    LDX #10  ; color
    STX $02
    LDX #1   ; up
    STX $04
    LDX #2   ; down 
    STX $05
    LDX #4   ; left
    STX $06
    LDX #8   ; right
    STX $07

    JMP Move

ClearZeroPage:
    LDA $00
    STA $0200,X
    INX
    BNE ClearZeroPage
    RTS

RandomStartColor:
    LDA $FE
    STA $0200,X
    INX
    BNE RandomStartColor
    RTS
    
Move:
    LDA $4000
    CMP $04
    BEQ MoveUp
    LDA $4000
    CMP $05
    BEQ MoveDown
    LDA $4000
    CMP $06
    BEQ MoveLeft
    LDA $4000
    CMP $07
    BEQ MoveRight

SetCell:
    JSR Position_XY
    LDA $02
    STA $0200,X
    JMP Move



MoveDown:
    JSR ClearLastCell
    LDA $01
    ADC #1
    JSR ClearLeftHalfByte
    STA $01
    CLC
    JMP SetCell

MoveUp:
    JSR ClearLastCell
    SEC
    LDA $01
    SBC #1
    JSR ClearLeftHalfByte
    STA $01
    CLC
    JMP SetCell

MoveRight:
    JSR ClearLastCell
    LDA $00
    ADC #1
    JSR ClearLeftHalfByte
    STA $00
    CLC
    JMP SetCell

MoveLeft:
    JSR ClearLastCell
    SEC
    LDA $00
    SBC #1
    JSR ClearLeftHalfByte
    STA $00
    CLC
    JMP SetCell

Position_XY:
    CLC
    LDA #0
    ADC $01
    ASL A
    ASL A
    ASL A
    ASL A
    ADC $00
    STA $03
    LDX $03
    RTS

ClearLastCell:
    JSR Position_XY
    LDA #0
    STA $0200,X
    RTS

ClearLeftHalfByte:
    ASL A
    ASL A
    ASL A
    ASL A
    LSR A
    LSR A
    LSR A
    LSR A
    RTS

.goto $FFFA
.dw start ; non maskable
.dw start ; reset  
.dw start ; interrupt  