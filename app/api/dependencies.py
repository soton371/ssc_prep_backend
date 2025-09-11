def getCurrentUser(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credential", headers={"WWW-Authenticate": "Bearer"})

    verifyToken = verifyAccessToken(token, credential_exception)

    user=db.query(auth_model.User).filter(auth_model.User.id == verifyToken.id).first()

    if not user:
        raise credential_exception
    
    return user